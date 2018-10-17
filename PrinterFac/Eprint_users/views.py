from django.shortcuts import render, redirect
from django.contrib import messages
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
    return render(request, 'Eprint_users/register.html', {'form' : form})

def history(request):
    return render(request, 'Eprint_users/history.html')


def PrintUpload(request):
    if request.method == 'POST':
        form = PrintForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('baseApp-home')
    else:
        form = PrintForm()
    return render(request, 'Eprint_users/upload.html', {'form': form})
