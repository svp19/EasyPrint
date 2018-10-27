from django import forms
from Eprint_users.models import PrintDocs


class UpdateForm(forms.ModelForm):
    class Meta:
        model = PrintDocs
        fields = ['task_by', 'completed', 'paid', 'collected', 'id']
