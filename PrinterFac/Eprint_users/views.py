import datetime
import os
import smtplib
import subprocess
import requests
from background_task.models import Task
from django.views.decorators.csrf import csrf_exempt
from pdfrw import PdfReader, PdfWriter
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import PrintForm, UserRegisterForm, ProfileForm, ConfirmForm
from .models import Profile, PrintDocs
from PyPDF2 import PdfFileReader
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from Eprint_admin.models import RatePerPage
from django.conf import settings
import razorpay
from background_task import background

# Media Upload Server
media_upload_url = settings.EASY_PRINT_MEDIA_UPLOAD_URL


@background(schedule=20)
def mark_completed(user_id):
    print("Enter Background mark")
    run_queue = subprocess.run(["lpq"], encoding='utf-8', stdout=subprocess.PIPE)
    output = run_queue.stdout

    # Update the objects which aren't completed(to be marked as completed) and not in the print queue
    s = [line.split() for line in output.split('\n')]
    s = s[2:]
    pending = []

    for row in s:
        try:
            if len(row) >= 4 and int(row[1]) == user_id:
                pending.append(int(row[3]))
        except ValueError:  # Someone else printed, hence row[3] may have a string of the user and we should ignore it
            pass

    user = User.objects.get(pk=user_id)
    qset = PrintDocs.objects.filter(task_by=user, completed=False).exclude(id__in=pending)
    doc_names = [doc.file_name for doc in qset]
    # Print documents updated in log
    print(doc_names)
    # Update documents in database
    PrintDocs.objects.filter(task_by=user, completed=False).exclude(id__in=pending).update(completed=True)
    # Send email notification to user if document printed.
    doc_names_str = ', '.join(doc_names)
    if len(doc_names) > 0:
        notify_user(user_id, doc_names_str)


def notify_user(user_id, doc_names):
    # Mark printed docs as completed
    mark_completed(user_id)

    user = User.objects.get(pk=user_id)
    print('Notification, HERE I COME!!!')
    print(user.email)
    print(user)
    mail_subject = 'EasyPrint: Document Printed Successfully'
    body = 'Dear {}, \nYour document(s):{} has been printed and is ready for collection. Please collect it' \
           ' from the Printer Room, Library, IIT Dharwad.' \
           'Thank You for using EasyPrint services. \nEasyPrint, IIT Dharwad'.format(user.username, doc_names)
    to_email = user.email
    server = smtplib.SMTP_SSL("smtp.googlemail.com", 465)
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    final_email = 'Subject: {} \n{}'.format(mail_subject, body)
    server.sendmail(settings.EMAIL_HOST_USER, to_email, final_email)
    print('Sent Notif')


def subset_pdf(inp_file, ranges):  # Create PDF with subset pages

    ranges = ranges.split(' ')

    for x in ranges:  # If ranges is something like a word or negative
        for y in x.split('-'):
            try:
                int(y)
            except ValueError:
                return -1

    ranges = ([int(y) for y in x.split('-')] for x in ranges)
    pages = PdfReader(inp_file).pages
    out_data = PdfWriter(inp_file)
    num_pages = 0
    try:
        for one_range in ranges:
            one_range = (one_range + one_range[-1:])[:2]
            for page_num in range(one_range[0], one_range[1] + 1):
                out_data.addpage(pages[page_num - 1])
                num_pages += 1
    except IndexError:  # If user gave invalid pages
        return -1
    out_data.write()
    return num_pages


def register(request):
    if request.user.is_authenticated:  # If user is logged in
        return redirect('baseApp-home')
    else:
        if request.method == 'POST':
            user_form = UserRegisterForm(request.POST)  # Populate form with instance submitted by user
            profile_form = ProfileForm()

            if user_form.is_valid():
                user = user_form.save(commit=False)

                user.is_active = False
                user.save()

                # Send account activation link to email
                current_site = get_current_site(request)
                body = render_to_string('Eprint_users/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })

                mail_subject = 'Activate your EasyPrint account.'
                to_email = user_form.cleaned_data.get('email')
                server = smtplib.SMTP_SSL("smtp.googlemail.com", 465)
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                final_email = 'Subject: {}{}'.format(mail_subject, body)
                server.sendmail(settings.EMAIL_HOST_USER, to_email, final_email)

                return render(request, 'ground/check_ack.html', {'activate': True})
                # profile_form = ProfileForm(request.POST, instance=user)
                # profile_form.save()
                # username = user_form.cleaned_data.get('username')
                # messages.success(request, f'Your account has been created successfully, {username}!')
                # return redirect('baseApp-home')

        else:
            user_form = UserRegisterForm()
            profile_form = ProfileForm()

        return render(request, 'Eprint_users/register.html', {'user_form': user_form, 'profile_form': profile_form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        if check_faculty(user.email):
            user.profile.is_faculty = True
            user.profile.save()

        return render(request, 'ground/check_ack.html', {'valid_registration': True})
    else:
        return render(request, 'ground/check_ack.html', {'valid_registration': False})


@login_required
def history(request):
    filter_by = request.GET.get('filter_by') or 'all'
    query = ''

    # # Get printer queue
    # run_queue = subprocess.run(["lpq"], encoding='utf-8', stdout=subprocess.PIPE)
    # output = run_queue.stdout
    #
    # # Update the objects which aren't completed(to be marked as completed) and not in the print queue
    # s = [line.split() for line in output.split('\n')]
    # s = s[2:]
    # pending = []
    # for row in s:
    #     try:
    #         if len(row) >= 4 and int(row[1]) == request.user.id:
    #             pending.append(int(row[3]))
    #     except ValueError:  # Someone else printed, hence row[3] may have a string of the user and we should ignore it
    #         pass
    #
    # PrintDocs.objects.filter(task_by=request.user, completed=False).exclude(id__in=pending).update(completed=True)

    # Checking for search query
    if request.GET.get('query'):
        query = request.GET.get('query')
    docs = PrintDocs.objects.filter(file_name__icontains=query, is_confirmed=True, task_by=request.user).order_by(
        '-date_uploaded')

    # Filter_by_here [ Spaghetti Code ToClean]
    if filter_by == 'paid':
        docs = docs.filter(paid="True")
    elif filter_by == 'collected':
        docs = docs.filter(collected="True")
    elif filter_by == "completed":
        docs = docs.filter(completed="True")

    if len(docs) > 0 or request.GET.get('query') or request.GET.get('filter_by'):
        show_table = True
    else:
        show_table = False

    return render(request, 'Eprint_users/history.html',
                  {'tasks': docs, 'query': query, 'filter_by': filter_by, 'show_table': show_table})


@login_required
def profile(request):
    profile_form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()

    return render(request, 'Eprint_users/profile.html', {'form': profile_form})


@csrf_exempt
def bill(request):
    if request.method == 'POST':

        username = request.POST.get('hidden')
        unpaid = PrintDocs.objects.filter(task_by__username=username, completed=True, paid=False, is_confirmed=True)
        amount_due = str(int(sum([i.price for i in unpaid]) * 100))

        client = razorpay.Client(auth=(settings.API_KEY, settings.API_PASS))
        client.set_app_details({"title": "PrinterFac", "version": "2.0"})

        payment_id = request.POST.get("razorpay_payment_id")
        client.payment.capture(payment_id, amount_due)
        unpaid.update(paid=True)

        return redirect('users-bill')

    else:
        unpaid = request.user.printdocs_set.filter(completed=True, paid=False, is_confirmed=True)
        amount_due = int(sum([i.price for i in unpaid]) * 100)

        return render(request, 'Eprint_users/bill.html',
                      {'not_paid_tasks': unpaid, 'total_due': amount_due, 'total_due_rupee': amount_due / 100,
                       'dict_username': request.user.username, 'api_key': settings.API_KEY})


@login_required
def print_upload(request):
    # Define const Price here
    rate_per_page_bw = RatePerPage.objects.first().rppBW
    rate_per_page_c = RatePerPage.objects.first().rppC

    if request.method == 'POST':

        form = PrintForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():

            # Getting number of pages
            if request.POST.get('description').lower() != 'all':
                num_pages = subset_pdf(request.FILES['document'], request.POST.get('description'))
            else:
                pdf_file = request.FILES['document'].open()
                num_pages = PdfFileReader(pdf_file, strict=False).getNumPages()

            # Raising error
            form = PrintForm(request.POST, request.FILES, user=request.user)
            if num_pages == -1:
                form.add_error('description', "Invalid page specification")
                return render(request, 'Eprint_users/upload.html', {'form': form})

            # Upload to database
            my_form = form.save(False)
            my_form.task_by = User.objects.get(username=request.user)
            my_form.file_name = request.FILES['document'].name
            # ground_file_name = my_form.document.name.split('/')[-1]

            # Count Number Of Pages and calc Price
            my_form.num_pages = num_pages
            rate_per_page = rate_per_page_bw
            if request.POST.get('colour'):
                rate_per_page = rate_per_page_c
            my_form.price = float(request.POST.get('copies')) * num_pages * rate_per_page

            # Generate order id
            my_form.order_id = datetime.datetime.now().strftime('%S%M%I%d%m%Y') + str(request.user.pk)

            my_form.save()

            return redirect('users-confirm')

    else:
        form = PrintForm(user=request.user)

    return render(request, 'Eprint_users/upload.html', {'form': form})


@login_required
def confirm(request):
    # Redirects home if no tasks pending confirmation
    print_doc = request.user.printdocs_set.last()
    if print_doc is None or print_doc.is_confirmed is True:
        return redirect('baseApp-home')

    form = ConfirmForm(instance=print_doc)
    form.is_confirmed = False

    if request.method == "POST":
        form = ConfirmForm(request.POST, instance=print_doc)

        user = User.objects.get(username=request.user)
        if form.is_valid():
            if request.POST.get('is_confirmed'):

                # Uploading to another Server
                if not user.profile.is_faculty:
                    files = open(print_doc.document.url, 'rb')
                    request_sender = requests.post(media_upload_url,
                                                   files={'fileToUpload': files},
                                                   data={'safe_url': request.user.profile.hash_url.hex})

                    if request_sender.status_code != 200:
                        # form.add_error('is_confirmed', "File may exceed")
                        return redirect('users-upload')

                # Update billing information
                new_amount_due = float(print_doc.price) + float(user.profile.amount_due)
                Profile.objects.filter(user=request.user).update(amount_due=new_amount_due)

                # Printing the job
                cmd = "lp"
                args = ["-U " + str(request.user.id)]
                args += ["-n " + str(print_doc.copies)]
                args += ["-t " + str(print_doc.id)]
                args += [print_doc.document.name]
                # args += ["-d " + settings.EASY_PRINT_PRINTER_NAME]  # Not working for now
                subprocess.run([cmd, *args], encoding='utf-8', stdout=subprocess.PIPE)

                # Delete file if user is faculty for maintaining confidentiality
                if user.profile.is_faculty:
                    file_path = print_doc.document.name
                    if os.path.isfile(file_path):
                        os.remove(file_path)

                # Launch Background to check if docs printed
                run_till = datetime.datetime.now() + datetime.timedelta(days=1)
                mark_completed(request.user.id, repeat=Task.HOURLY, repeat_until=run_till,
                               verbose_name=f"Notify user:{user.id} hourly", creator=user)

            form.save()
            return redirect('baseApp-home')

    return render(request, 'Eprint_users/confirm.html', {'form': form, 'price': print_doc.price})


def check_faculty(email):
    try:
        int(email.split('@')[0])
    except ValueError:
        return True
    return False
