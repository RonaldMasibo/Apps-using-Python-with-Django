from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages


# Create your views here.

def index(request):
    if request.method == 'POST':
        UserName = request.POST['Uname']
        FirstName = request.POST['Fname']
        LastName = request.POST['Lname']
        Email = request.POST['Email']
        Password = request.POST['Password1']
        Password2 = request.POST['Password2']

        if Password == Password2:
            if User.objects.filter(username = UserName).exists():
                messages.info(request, 'Username is already in use!!')
                return redirect('')
            elif User.objects.filter(email = Email).exists():
                messages.info(request, 'Email is already in use!!')
                return redirect('')
            else:
                user = User.objects.create_user(
                    username = UserName,
                    first_name = FirstName,
                    last_name = LastName,
                    email = Email,
                    password = Password
                )
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords do NOT match!!')
            return redirect('')
    else:
        return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        Email = request.POST['Email']
        Password = request.POST['Password']

        user = auth.authenticate(
            email = Email,
            password = Password
        )

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'INVALID details!!')
            return redirect('login')
    else:
        return render(request, 'login.html')


