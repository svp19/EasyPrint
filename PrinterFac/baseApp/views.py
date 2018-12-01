# This is where the view logic of the page is made up
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Eprint_users.models import PrintDocs
from . import checksum


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
        context = {"MID": "fDlkIy64148311435937", "TXN_AMOUNT": str(doc.price), "ORDER_ID": str(doc.order_id),
                   "CUST_ID": 'CUST001', "CHANNEL_ID": "WEB", "INDUSTRY_TYPE_ID": "Retail",
                   "WEBSITE": "WEB_STAGING"}
        checksum_hash = checksum.generate_checksum(context, "Z1IzyJW2BvkU8pWX")
        print(context)
        print(checksum_hash)
        print(checksum.verify_checksum(context, "Z1IzyJW2BvkU8pWX", checksum_hash))
        return render(request, "ground/payment.html",
                      {'CHECKSUMHASH': checksum_hash, "MID": "fDlkIy64148311435937", "TXN_AMOUNT": str(doc.price),
                       "ORDER_ID": str(doc.order_id),
                       "CUST_ID": 'CUST001', "CHANNEL_ID": "WEB", "INDUSTRY_TYPE_ID": "Retail",
                       "WEBSITE": "WEB_STAGING",
                       "CALLBACK_URL": "http://127.0.0.1/PaytmKit/pgResponse.php"})
    else:
        return redirect('baseApp-home')


def login(request):
    if request.user.is_authenticated:  # Redirect to home if already logged in
        return redirect('baseApp-home')
    else:
        return redirect('loginPage')


def about(request):
    return render(request, 'ground/about.html', {'title': 'About'})
