from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import RegisteredUsersForm
from .models import RegisteredUsersModel
from django.contrib.auth.hashers import make_password # For saving a hashed password

# Create your views here.

def base(request):
    return render(request, 'base.html')


def register(request):

    if request.method == 'POST':

        form = RegisteredUsersForm(request.POST)

        if form.is_valid():

            First_Name = form.cleaned_data['First_Name']
            Middle_Name = form.cleaned_data['Middle_Name']
            Last_Name = form.cleaned_data['Last_Name']
            Email = form.cleaned_data['Email']
            Password = form.cleaned_data['Password']
            Password2 = form.cleaned_data['Password2']

            if Password == Password2:
                if RegisteredUsersModel.objects.filter(Email=Email).exists():
                    messages.info(request, 'Email is already in use..Use another one!!')
                    return redirect('register')
                else:
                    Hashed_Password = make_password(Password) # Hash the Plain Text Password
                    NewUser = RegisteredUsersModel.objects.create(
                        First_Name = First_Name,
                        Middle_Name = Middle_Name,
                        Last_Name = Last_Name,
                        Email = Email,
                        Password = Hashed_Password
                    )
                    NewUser.save()
                    messages.success(request, 'Your account has been successfully created!!')
                    return redirect('login')
            else:
                messages.error(request, 'Passwords DO NOT match!!!')
                return redirect('register')
    else:
        form = RegisteredUsersForm()
    return render(request, 'register.html', {'form':form})



def login(request):
    return render(request, 'login.html')
    

#def home(request)


#def profile(request)

