import os

from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from Eprint_admin.models import RatePerPage
from Eprint_users.models import PrintDocs, Profile
from .forms import UpdateForm, ChangeRate
from django.contrib.admin.views.decorators import user_passes_test


@user_passes_test(lambda u: u.is_staff, login_url='login')
def tasks(request):
    # If query exists in get variables
    if request.GET.get('query'):
        query = request.GET.get('query')
        docs = PrintDocs.objects.filter(Q(file_name__icontains=query) | Q(task_by__username__icontains=query),
                                        is_confirmed=True)
        # Q objects are a way to OR queries together
    else:
        docs = PrintDocs.objects.filter(is_confirmed=True)
    forms = []
    edits = {x: False for x in range(len(docs))}

    if request.method == 'POST':
        i = -1
        for doc in docs:
            i += 1
            temp_doc = PrintDocs.objects.filter(id=doc.id).first()
            if request.POST.get('completed' + str(i)) is None:
                if temp_doc.completed is True:
                    temp_doc.completed = False
                    edits[i] = True
            elif request.POST.get('completed' + str(i)) == 'on':
                if temp_doc.completed is False:
                    temp_doc.completed = True
                    edits[i] = True
            if request.POST.get('paid' + str(i)) is None:  # Not Possible
                if temp_doc.paid is True:
                    temp_doc.paid = False
                    edits[i] = True
            if request.POST.get('paid' + str(i)) == 'on':
                if temp_doc.paid is False:
                    temp_doc.paid = True
                    edits[i] = True
                    temp_pro = Profile.objects.filter(id=temp_doc.task_by.profile.id).first()
                    temp_pro.amount_due -= temp_doc.price
                    temp_pro.save()
            if request.POST.get('collected' + str(i)) is None:
                if temp_doc.collected is True:
                    temp_doc.collected = False
                    edits[i] = True
            elif request.POST.get('collected' + str(i)) == 'on':
                if temp_doc.collected is False:
                    temp_doc.collected = True
                    edits[i] = True
            temp_doc.save()

        messages.success(request, 'Successfully updated {0} document(s)'.format(sum(edits.values())))
        return redirect('admin-tasks')
    else:
        for doc in docs:
            temp_form = UpdateForm(instance=doc)
            forms.append(temp_form)

        ids = [i for i in range(len(forms))]
        ground_file_names = [os.path.basename(i.document.name) for i in docs]
        context = zip(docs, forms, ids, ground_file_names)
        curr_dir = os.getcwd().replace('\\', '/')
        return render(request, 'Eprint_admin/tasks.html',
                      {'context': context, 'curr_dir': curr_dir, 'host': settings.EASY_PRINT_MEDIA_HOST})


@user_passes_test(lambda u: u.is_staff, login_url='login')
def update_prices(request):
    if request.method == 'POST':
        form = ChangeRate(request.POST, instance=RatePerPage.objects.first())
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated prices')
            return redirect('admin-update')
    else:
        form = ChangeRate(instance=RatePerPage.objects.first())
        return render(request, 'Eprint_admin/update.html', {'update_form': form})
