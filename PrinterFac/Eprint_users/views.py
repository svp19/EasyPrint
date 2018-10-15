from django.shortcuts import render
from . models import PrintDocs

def history(request):
    return render(request, 'Eprint_users/history.html', {'tasks': PrintDocs.objects.all()})
