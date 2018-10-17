from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from . forms import PrintForm, UserRegisterForm
# from . models import Bill {'tasks': Bill.objects.all()}


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created successfully, {username}!')
            return redirect('baseApp-home')

    else:
        form = UserRegisterForm()
    return render(request, 'Eprint_users/register.html', {'form': form})


def history(request):
    return render(request, 'Eprint_users/history.html')


def print_upload(request):
    if request.method == 'POST':
        form = PrintForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            my_form = form.save(False)
            my_form.task_by = User.objects.get(username=request.user)
            my_form.save()
            return redirect('baseApp-home')
    else:
        form = PrintForm(user=request.user)
    return render(request, 'Eprint_users/upload.html', {'form': form})
