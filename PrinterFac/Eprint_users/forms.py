from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import PrintDocs


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    # phone_num = forms.CharField(max_length=11) 'phone_num',

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', ]

class PrintForm(forms.ModelForm):
    class Meta:
        model = PrintDocs
        fields = ['description', 'document', 'colour', 'copies', ]
