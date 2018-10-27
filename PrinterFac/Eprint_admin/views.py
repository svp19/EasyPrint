from django.shortcuts import render, redirect
from Eprint_users.models import PrintDocs
from . forms import UpdateForm


def tasks(request):
    docs = PrintDocs.objects.all()
    forms = []
    if request.method == 'POST':
        i = -1
        for doc in docs:
            i += 1
            temp_doc = PrintDocs.objects.filter(id=doc.id).first()

            if request.POST.get('completed' + str(i)) is None:
                temp_doc.completed = False
            elif request.POST.get('completed' + str(i)) == 'on':
                temp_doc.completed = True
            if request.POST.get('paid' + str(i)) is None:
                temp_doc.paid = False
            elif request.POST.get('paid' + str(i)) == 'on':
                temp_doc.paid = True
            if request.POST.get('collected' + str(i)) is None:
                temp_doc.collected = False
            elif request.POST.get('collected' + str(i)) == 'on':
                temp_doc.collected = True
            temp_doc.save()

            temp_form = UpdateForm(request.POST, instance=temp_doc)
            forms.append(temp_form)
        return redirect('admin-tasks')
    else:
        for doc in docs:
            temp_form = UpdateForm(instance=doc)
            forms.append(temp_form)

        ids = [i for i in range(len(forms))]
        context = zip(docs, forms, ids)
        return render(request, 'Eprint_admin/tasks.html', {'context': context})
