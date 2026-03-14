from django.shortcuts import render, redirect, get_object_or_404
from .models import People
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm, PersonForm
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

    # Every single person being stored in the DB
    people = People.objects.all()

    if request.method == "POST":

        # Creating instance of model form
        form = PersonForm(request.POST, request.FILES)

        # Add People
        if "add_people" in request.POST:
            if form.is_valid():
                form.save()
                return redirect('main')
        
        # Edit People
        elif "edit_people" in request.POST:

            # Get the ID of the person first
            person_id = request.POST.get("person_id")
            
            # Fetch the object related to the passed ID
            obj = get_object_or_404(People, id=person_id)

            # Pass the object as an instance in form
            form = PersonForm(request.POST, request.FILES, instance=obj)

            # Save the edited info
            if form.is_valid():
                form.save()
                return redirect('main')
        
        # Delete People
        elif "delete_person" in request.POST:
            # Get the ID of the person first
            person_id = request.POST.get("person_id")
            
            obj = get_object_or_404(People, id=person_id)
            obj.delete()
            return redirect('main')
        
        # Delete EVERYTHING at once
        elif "delete_all" in request.POST:
            people.delete()
            return redirect('main')

    else:
        form = PersonForm()
    
    welcome_message = f'Welcome {request.user}'
    return render(request, 'home.html', {
        'welcoming_mess':welcome_message, 
        'people':people, 
        'person_form':form,
        'no_people':people.count()
    })

