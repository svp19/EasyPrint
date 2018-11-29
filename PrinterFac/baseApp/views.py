# This is where the view logic of the page is made up
import datetime
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Eprint_users.models import PrintDocs


@login_required
def home(request):
    # Delete unconfirmed tasks
    print_docs = PrintDocs.objects.filter(task_by=request.user, is_confirmed=False)
    for doc in print_docs:
        file_path = doc.document.name
        if os.path.isfile(file_path):
            os.remove(file_path)
    PrintDocs.objects.filter(task_by=request.user, is_confirmed=False).delete()

    return render(request, 'ground/home.html', {'title': 'Home', 'user': request.user})


@login_required
def payment(request):
    doc = PrintDocs.objects.filter(task_by=request.user, is_confirmed=True).last()

    if doc is not None:
        context = {'MID': 'fDlkIy64148311435937', 'TXN_AMOUNT': doc.price, 'ORDER_ID': doc.order_id,
                   'CUST_ID': str(request.user.pk).zfill(64)}
        return render(request, 'ground/payment.html', context)
    else:
        return redirect('baseApp-home')


def login(request):
    if request.user.is_authenticated:  # Redirect to home if already logged in
        return redirect('baseApp-home')
    else:
        return redirect('loginPage')


def about(request):
    return render(request, 'ground/about.html', {'title': 'About'})
