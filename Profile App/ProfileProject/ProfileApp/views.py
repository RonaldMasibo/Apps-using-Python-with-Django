from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm

# from django.contrib.auth.hashers import make_password # For making a hashed password

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def base(request):
    return render(request, 'base.html')


def register(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created!!')
            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form':form})


def doLogin(request):

    if request.method == 'POST':

        username = request.POST['username']
        Password = request.POST['password']

        user = authenticate(
            request,
            username = username,
            password = Password
        )

        if user is not None:
            form = login(request, user)
            messages.success(request, f'Welcome {user.username} !!')
            return redirect('main')
        else:
            messages.info(request, f'The Account does not exist!!!')

    form = AuthenticationForm()
        
    return render(request, 'login.html', {'form':form})


@login_required
def doLogout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def main(request):
    welcome_message = f'Welcome {request.user}'
    return render(request, 'home.html', {'welcoming_mess':welcome_message})


#def profile(request)

