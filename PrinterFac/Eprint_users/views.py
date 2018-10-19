from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from . forms import PrintForm, UserRegisterForm, ProfileForm
from .models import Profile
from PyPDF2 import PdfFileReader

'''pip install PyPDF2'''


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid():
            user_form.save()
            profile_form.save()
            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created successfully, {username}!')
            return redirect('baseApp-home')

    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()
    return render(request, 'Eprint_users/register.html', {'user_form': user_form, 'profile_form': profile_form})


def history(request):
    return render(request, 'Eprint_users/history.html')


def print_upload(request):

    # Define const Price here
    rate_per_page = 3.00

    if request.method == 'POST':
        form = PrintForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():

            # Upload to database
            my_form = form.save(False)
            my_form.task_by = User.objects.get(username=request.user)

            # Count Number Of Pages and calc Price
            pdf_file = request.FILES['document'].open()
            num_pages = PdfFileReader(pdf_file, strict=False).getNumPages()
            my_form.num_pages = num_pages
            my_form.price = float(request.POST.get('copies')) * num_pages * rate_per_page
            my_form.save()

            # Update billing information
            user = User.objects.get(username=request.user)
            new_amount_due = float(my_form.price) + float(user.profile.amount_due)
            Profile.objects.filter(user=request.user).update(amount_due=new_amount_due)
            return redirect('baseApp-home')
    else:
        form = PrintForm(user=request.user)
    return render(request, 'Eprint_users/upload.html', {'form': form})
