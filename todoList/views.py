from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.models import User
from todoList.forms import TODOForm, TODOForm_Admin, LangForm
from todoList.models import TODO, Profile
from django.views.decorators.csrf import csrf_exempt
from .models import *
import random
from .mixins import OtpHandler
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TODO_Serializer
from django.conf import settings
from todoList.tasks import *


# Create your views here.
@login_required(login_url='login')
@api_view(['GET'])
def view_todo(request, id): 
    todo = get_object_or_404(TODO, pk=id)
    serializer = TODO_Serializer(todo)
    return Response(serializer.data)

'''
def add_phone_number_to_verified_list(phone_number):
    #api call to add phone number to verified list of twilio and verify it using otp
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    validation_request = client.validation_requests.create(
        friendly_name="Third Party VOIP Number",
        phone_number="+14158675310",
        status_callback="https://somefunction.twil.io/caller-id-validation-callback",
    )
    pass
'''
def pass_login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {
            "form": form
        }
        return render(request, 'pass_login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                return redirect('home')
        else:
            context = {
                "form": form
            }
            return render(request, 'pass_login.html', context=context)


def login(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        if not Profile.objects.filter(phone_number=phone_number).exists():
            return redirect('signup')
        
        profile = Profile.objects.get(phone_number=phone_number)
        profile.otp = random.randint(1000, 9999)
        profile.save()
        
        otp_handler = OtpHandler(phone_number=phone_number, otp=profile.otp)
        otp_handler.send_otp_on_phone()
        
        return redirect(f'/otp/{profile.uid}')
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})
        
        user = User(username=username)
        user.set_unusable_password()  # This sets a flag indicating the user has no password
        user.save()
        
        profile = Profile.objects.create(user=user, phone_number=phone_number)
        return redirect('login')
    else:
        if request.method == 'GET':
            return render(request, 'signup.html')
    
    return render(request, 'signup.html')


def pass_signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form": form
        }
        return render(request, 'pass_signup.html', context=context)
    else:
        form = UserCreationForm(request.POST)
        context = {
            "form": form
        }
        if form.is_valid():
            user = form.save()
            if user is not None:
                return redirect('pass_login')
        else:
            return render(request, 'pass_signup.html', context=context)


@login_required(login_url='login')
def signout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        if request.user.is_superuser:
            form = TODOForm_Admin(request.POST)
            if form.is_valid():
                todo = form.save()
                return redirect("home")
            else:
                return render(request, 'index.html')
        else:
            form = TODOForm(request.POST)
            if form.is_valid():
                todo = form.save(commit=False)
                todo.user = user
                todo.save()
                return redirect("home")
            else:
                return render(request, 'index.html')
    else:
        return redirect("home")

@login_required(login_url='login')
def home(request):

    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        form_admin = TODOForm_Admin()
        langform = LangForm()
    
        if request.user.is_superuser:
            todos = TODO.objects.all()
            if lang.objects.filter(user=user).exists():
                current_language=lang.objects.get(user=user).language
            else:
                current_language='de'
            context = {
            'form': form,
            'form_admin': form_admin,
            'todos': todos,
            'langForm': langform,
            'current_language': current_language
            }
            return render(request, 'index.html', context)
        else:
            todos = TODO.objects.filter(user=user)
            if lang.objects.filter(user=user).exists():
                current_language=lang.objects.get(user=user).language
            else:
                current_language='de'
            context = {
            'form': form,
            'form_admin': form_admin,
            'todos': todos,
            'langForm': langform,
            'current_language': current_language
            }
            return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')

@login_required(login_url='login')
def delete_todo(request, id):
    TODO.objects.get(pk=id).delete()
    return redirect('home')

def change_status(request, id, status):
    todo = TODO.objects.get(pk=id)
    todo.status = status
    todo.save()
    return redirect('home')

def otp(request, uid):
    if request.method == 'POST':
        profile = Profile.objects.get(uid=uid)
        otp = request.POST.get('otp')
        if int(otp) == profile.otp:
            loginUser(request, profile.user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    return render(request, 'otp.html')

def set_language(request):
    if request.method == 'POST':
        form = LangForm(request.POST)
        if form.is_valid():
            lang_obj = form.save(commit=False)
            lang_obj.user = request.user
            lang.objects.update_or_create(
                user=lang_obj.user,
                defaults={'language': lang_obj.language}
            )

            return redirect('home')
    else:
        lang_instance = lang.objects.filter(user=request.user).first()
        initial_data = {'language': lang_instance.language} if lang_instance else {}
        form = LangForm(initial=initial_data)
    
    return render(request, 'set_language.html', {'langForm': form})