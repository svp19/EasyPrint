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
    docs = PrintDocs.objects.filter(task_by=request.user, is_confirmed=True, paid=False)
    amount_due = sum([i.price for i in docs])

    if amount_due > 0:
        context = {"MID": "fDlkIy64148311435937", "TXN_AMOUNT": str(amount_due),
                   "ORDER_ID": datetime.datetime.now().strftime('%S%I%H%d%m%Y') + str(docs.last().pk),
                   "CUST_ID": 'CUST001', "CHANNEL_ID": "WEB", "INDUSTRY_TYPE_ID": "Retail",
                   "WEBSITE": "WEB_STAGING"}
        return render(request, "ground/payment.html", context)
    else:
        return redirect('baseApp-home')


def login(request):
    if request.user.is_authenticated:  # Redirect to home if already logged in
        return redirect('baseApp-home')
    else:
        return redirect('loginPage')


def about(request):
    return render(request, 'ground/about.html', {'title': 'About'})
