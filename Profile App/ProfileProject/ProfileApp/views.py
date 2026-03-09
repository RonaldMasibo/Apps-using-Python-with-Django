from django.shortcuts import render, redirect, get_object_or_404
from .models import People
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
        # Add People
        if "add_people" in request.POST:

            # Retrieve inputs from the HTML form
            f_name = request.POST.get('first_name')
            m_name = request.POST.get('middle_name')
            l_name = request.POST.get('last_name')
            prof_img = request.POST.get('profile_img')
            phone_no = request.POST.get('phone_number')
            
            # Save contents into the DB
            People.objects.create(
                f_name = f_name,
                m_name = m_name,
                l_name = l_name,
                prof_img = prof_img,
                phone_no = phone_no,
            )

            return redirect('main')
        
        # Edit People
        if "edit_people" in request.POST:

            # Retrieving updated details on People
            people_id = request.POST.get('people_id')
            new_fname = request.POST.get('new_fname')
            new_mname = request.POST.get('new_mname')
            new_lname = request.POST.get('new_lname')
            new_image = request.POST.get('new_image')
            new_phoneNo = request.POST.get('new_phoneNo')

            # Saving updated details on the DB
            updated_person = get_object_or_404(People, id=people_id)
            updated_person.f_name = new_fname
            updated_person.m_name = new_mname
            updated_person.l_name = new_lname
            updated_person.prof_img = new_image
            updated_person.phone_no = new_phoneNo
            updated_person.save()

            return redirect('main')
        
        # Delete People
        if "delete_people" in request.POST:
            people_id = request.POST.get('people_id')
            person = get_object_or_404(People, id=people_id)
            person.delete()
            return redirect('main')
        
        # Delete EVERYTHING at once
        if "delete_all" in request.POST:
            People.objects.all().delete()
            return redirect('main')

    welcome_message = f'Welcome {request.user}'
    return render(request, 'home.html', {'welcoming_mess':welcome_message, 'people':People, 'no_people':People.count()})

