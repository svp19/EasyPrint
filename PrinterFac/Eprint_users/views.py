from django.shortcuts import render
from . models import Bill

def history(request):
    return render(request, 'Eprint_users/history.html', {'tasks': Bill.objects.all()})
