from django.contrib import messages
from django.shortcuts import render, redirect
from Eprint_admin.models import RatePerPage
from Eprint_users.models import PrintDocs, Profile
from . forms import UpdateForm, ChangeRate
from django.contrib.admin.views.decorators import user_passes_test


@user_passes_test(lambda u: u.is_staff, login_url='login')
def tasks(request):
    docs = PrintDocs.objects.all()
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
            # if request.POST.get('paid' + str(i)) is None:  # Not Possible
            #     if temp_doc.paid is True:
            #         temp_doc.paid = False
            #         edits[i] = True
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
        context = zip(docs, forms, ids)
        return render(request, 'Eprint_admin/tasks.html', {'context': context})


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
