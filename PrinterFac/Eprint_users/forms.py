from django import forms
from . models import PrintDocs


class PrintForm(forms.ModelForm):
    class Meta:
        model = PrintDocs
        fields = ['description', 'document', 'colour', 'copies',]