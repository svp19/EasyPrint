from django.shortcuts import render, redirect
from . forms import PrintForm
# from . models import Bill {'tasks': Bill.objects.all()}


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
