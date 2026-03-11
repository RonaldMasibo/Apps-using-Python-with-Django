

from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import People


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class PersonForm(forms.ModelForm):
    class Meta:
        model = People
        fields = ['f_name', 'm_name', 'l_name', 'prof_img', 'phone_no']