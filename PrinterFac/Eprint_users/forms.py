from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateField

from . models import PrintDocs
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    def clean_email(self):  # Define own cleaning method for organisations
        email_passed = self.cleaned_data.get('email')
        if not email_passed.endswith('@iitdh.ac.in'):
            raise forms.ValidationError("Invalid Email. Please register with your email registered to IIT Dharwad")

        return email_passed

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', ]


class ProfileForm(forms.ModelForm):
    birth_date = DateField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Profile
        fields = ('bio', 'birth_date')


class PrintForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PrintForm, self).__init__(*args, **kwargs)

        # Labels, help text and other field attributes customisation
        self.fields['description'].help_text = \
            'Enter the pages you want to select, for eg. "1 2-6 11-14 20" where (2-6 is inclusive of 2 and 6\
            ). Leave as \'All\' to print everything.'
        self.fields['description'].label = 'Pages'
        self.fields['description'].initial = 'All'

    def clean(self):  # Custom clean method for PDF files

        doc_passed = self.cleaned_data.get('document')
        doc_name = doc_passed.name  # Set PrintDoc name as doc_passed.name for further reference
        if not doc_name.endswith('.pdf'):
            self.add_error('description', "Please upload only PDF Files")
        return self.cleaned_data

    class Meta:
        model = PrintDocs
        fields = ['description', 'document', 'copies', ]


class ConfirmForm(forms.ModelForm):  # Form for confirming print task

    class Meta:
        model = PrintDocs
        fields = ['is_confirmed']

    def __init__(self, *args, **kwargs):
        super(ConfirmForm, self).__init__(*args, **kwargs)

        self.fields['is_confirmed'].label = 'I would like to confirm this print. '
