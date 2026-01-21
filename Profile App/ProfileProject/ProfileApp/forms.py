

from django import forms


class RegisteredUsersForm(forms.Form):
    First_Name = forms.CharField(max_length=100)
    Middle_Name = forms.CharField(max_length=100)
    Last_Name = forms.CharField(max_length=100)
    Email = forms.EmailField(max_length=50)
    Password = forms.CharField(widget=forms.PasswordInput())
    Password2 = forms.CharField(widget=forms.PasswordInput())


class LoginUsersForm(forms.Form):
    First_Name = forms.CharField(max_length=100)
    Email = forms.EmailField(max_length=50)
    Password = forms.CharField(widget=forms.PasswordInput())