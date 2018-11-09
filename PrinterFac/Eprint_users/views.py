from pdfrw import PdfReader, PdfWriter

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import PrintForm, UserRegisterForm, ProfileForm, ConfirmForm
from .models import Profile
from PyPDF2 import PdfFileReader
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from . tokens import account_activation_token
from django.core.mail import EmailMessage
from Eprint_admin.models import RatePerPage

'''
pip install PyPDF2
pip install pdfrw
'''


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
    except IndexError:
        return -1
    out_data.write()
    return num_pages


def register(request):
    if request.user.is_authenticated:
        return redirect('baseApp-home')
    else:
        if request.method == 'POST':
            user_form = UserRegisterForm(request.POST)
            profile_form = ProfileForm()
            if user_form.is_valid():
                user = user_form.save(commit=False)

                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                message = render_to_string('Eprint_users/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                mail_subject = 'Activate your blog account.'
                to_email = user_form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
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
        # return redirect('home')
        return render(request, 'ground/check_ack.html', {'valid_registration': True})
    else:
        return render(request, 'ground/check_ack.html', {'valid_registration': False})


@login_required
def history(request):
    return render(request, 'Eprint_users/history.html', {'tasks': request.user.printdocs_set.filter(is_confirmed=True)})


@login_required
def bill(request):
    unpaid = request.user.printdocs_set.filter(paid=False, is_confirmed=True)
    return render(request, 'Eprint_users/bill.html',
                  {'not_paid_tasks': unpaid,
                   'total_due': sum([i.price for i in unpaid])})


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

            # Count Number Of Pages and calc Price

            my_form.num_pages = num_pages
            rate_per_page = rate_per_page_bw
            if request.POST.get('colour'):
                rate_per_page = rate_per_page_c
            my_form.price = float(request.POST.get('copies')) * num_pages * rate_per_page

            my_form.save()

            # on confirm
            return redirect('users-confirm')

    else:
        form = PrintForm(user=request.user)
    return render(request, 'Eprint_users/upload.html', {'form': form})


@login_required
def confirm(request):

    print_doc = request.user.printdocs_set.last()  # Gets last uploaded document of user
    form = ConfirmForm(instance=print_doc)
    form.is_confirmed = False
    if request.method == "POST":
        form = ConfirmForm(request.POST, instance=print_doc)
        if form.is_valid():
            if request.POST.get('is_confirmed'):

                # Update billing information
                user = User.objects.get(username=request.user)
                new_amount_due = float(print_doc.price) + float(user.profile.amount_due)
                Profile.objects.filter(user=request.user).update(amount_due=new_amount_due)
            form.save()
            return redirect('baseApp-home')
    return render(request, 'Eprint_users/confirm.html', {'form': form, 'price': print_doc.price})
