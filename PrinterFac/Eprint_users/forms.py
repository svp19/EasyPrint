from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from validate_email import validate_email
from . models import PrintDocs
from .models import Profile

''' 
pip install validate_email
pip install py3DNS
'''


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    # phone_num = forms.CharField(max_length=11) 'phone_num',

    def clean_email(self):
        email_passed = self.cleaned_data.get('email')
        is_valid = validate_email(email_passed, verify=True)
        if '@iitdh.ac.in' not in email_passed:
            raise forms.ValidationError("Invalid Email. Please register with your email registered to IIT Dharwad")
        if not is_valid:
            raise forms.ValidationError("Sorry, this email is not registered with IIT Dharwad")
        return email_passed

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'birth_date')


class PrintForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PrintForm, self).__init__(*args, **kwargs)

    def clean_document(self):
        doc_passed = self.cleaned_data.get('document')
        doc_name = doc_passed.name
        if not doc_name.endswith('.pdf'):
            raise forms.ValidationError("Please upload only PDF Files")
        return doc_passed

    class Meta:
        model = PrintDocs
        fields = ['description', 'document', 'colour', 'copies', ]
