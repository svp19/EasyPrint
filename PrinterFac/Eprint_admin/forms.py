from django import forms
from Eprint_users.models import PrintDocs
from . models import RatePerPage


class UpdateForm(forms.ModelForm):
    class Meta:
        model = PrintDocs
        fields = ['task_by', 'completed', 'paid', 'collected', 'id']


class ChangeRate(forms.ModelForm):
    class Meta:
        model = RatePerPage
        fields = ['rppBW']

    def __init__(self, *args, **kwargs):
        super(ChangeRate, self).__init__(*args, **kwargs)
        self.fields['rppBW'].label = "Black and White"
        # self.fields['rppC'].label = "Colour"
        self.fields['rppBW'].help_text = "Per Page (One Side)"
        # self.fields['rppC'].help_text = "Per Page (One Side)"
