from django.forms import ModelForm, inlineformset_factory
from Eprint_users.models import PrintDocs
from django.contrib.auth.models import User


class UpdatePrintDocsForm(ModelForm):
    class Meta:
        model = PrintDocs
        fields = ['collected']
