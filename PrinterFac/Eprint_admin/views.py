from django.contrib.auth.models import User
from django.shortcuts import render
from django.forms import inlineformset_factory, modelformset_factory

from Eprint_users.models import PrintDocs


def tasks(request):
    all_docs = PrintDocs.objects.all()
    print_docs_form_set = modelformset_factory(PrintDocs, fields='__all__', extra=0, exclude=['document', 'description'])
    if request.method == "POST":
        formset = print_docs_form_set(request.POST, queryset=all_docs)
        for form in formset:
            form.fields['task_by'].widget.attrs['disabled'] = True
            form.fields['file_name'].widget.attrs['readonly'] = True
        if formset.is_valid():
            formset.save()
    else:
        formset = print_docs_form_set(queryset=all_docs)
    return render(request, 'Eprint_admin/alltasks.html', {'formset': formset})

