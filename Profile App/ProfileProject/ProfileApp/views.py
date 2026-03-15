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
        if "edit_people" in request.POST:

            # Get the ID of the person first
            person_id = request.POST.get("person_id")

            # Get the details of the update form
            new_fname = request.POST.get("f_name")
            new_mname = request.POST.get("m_name")
            new_lname = request.POST.get("l_name")
            new_profImg = request.FILES.get("prof_img")
            new_phoneNo = request.POST.get("phone_no")
            
            # Fetch the object related to the passed ID
            obj = get_object_or_404(People, id=person_id)

            # Save the edited info
            obj.f_name = new_fname
            obj.m_name = new_mname
            obj.l_name = new_lname
            obj.phone_no = new_phoneNo
            if obj.prof_img:
                obj.prof_img = new_profImg
            obj.save()

            return redirect('main')
        
        # Delete People
        if "delete_person" in request.POST:
            # Get the ID of the person first
            person_id = request.POST.get("person_id")
            
            obj = get_object_or_404(People, id=person_id)
            obj.delete()
            return redirect('main')
        
        # Delete EVERYTHING at once
        if "delete_all" in request.POST:
            people.delete()
            return redirect('main')

    form = PersonForm()
    
    welcome_message = f'Welcome {request.user}'
    return render(request, 'home.html', {
        'welcoming_mess':welcome_message, 
        'people':people, 
        'person_form':form,
        'no_people':people.count()
    })

