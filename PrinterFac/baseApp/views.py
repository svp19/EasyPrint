# This is where the view logic of the page is made up

from django.shortcuts import render

def home(request):
    return render(request, 'ground/home.html', {'title': 'Home'})


def about(request):
    return render(request, 'ground/about.html', {'title': 'About'})
