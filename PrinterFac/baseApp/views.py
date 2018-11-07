# This is where the view logic of the page is made up
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def home(request):
    return render(request, 'ground/home.html', {'title': 'Home'})


def login(request):
    if request.user.is_authenticated:
        return redirect('baseApp-home')
    else:
        return redirect('loginPage')


def about(request):
    return render(request, 'ground/about.html', {'title': 'About'})
