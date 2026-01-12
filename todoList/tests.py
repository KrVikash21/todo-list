from django.test import TestCase 
import pytest
from django.contrib.auth.models import User
from django.urls import reverse #reverse is used to get the URL of the view
from rest_framework.test import APIClient 
import datetime
import uuid 

from .models import TODO, Profile

# Create your tests here.

@pytest.mark.django_db  #this decorator will tell pytest to use the database
def test_home():
    # Create a user for authentication
    user = User.objects.create_user(username='testuser', password='testpassword')
    client = APIClient() #APIClient is a class that is used to make requests to the API
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('home')) #reverse is used to get the URL of the view,
    assert response.status_code == 200 #assert is a keyword used to check if the condition is true
    
    user.delete()
    assert User.objects.count() == 0
    

@pytest.mark.django_db
def test_login():
    client = APIClient()
    response = client.get(reverse('login')) 
    assert response.status_code == 200

@pytest.mark.django_db
def test_signup():
    client = APIClient()
    response = client.get(reverse('signup'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_pass_login():
    client = APIClient()
    response = client.get(reverse('pass_login'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_pass_signup():
    client = APIClient()
    response = client.get(reverse('pass_signup'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_todo():
    user = User.objects.create_user(username='testuser', password='testpassword')
    client = APIClient()
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('add_todo'))
    assert response.status_code == 200  
    
    user.delete()
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_signout():
    client = APIClient()
    response = client.get(reverse('signout'))
    assert response.status_code == 302 #302 is the status code for redirection 

@pytest.mark.django_db
def test_delete_todo():
    client = APIClient()
    response = client.get(reverse('delete_todo', kwargs={'id': 1})) #kwargs is used to pass the arguments to the view
    assert response.status_code == 302
    
    assert TODO.objects.count() == 0


@pytest.mark.django_db
def test_change_status():
    
    user = User.objects.create_user(username='testuser', password='testpassword')
    client = APIClient()
    client.login(username='testuser', password='testpassword')
    
    todo = TODO.objects.create(title='Test TODO', user=user, status='Pending')
    response = client.post(reverse('change_status', kwargs={'id': todo.id, 'status': 'Completed'}))

    assert response.status_code == 302    
    todo.refresh_from_db()
    assert todo.status == 'Completed'
    
    todo.delete()
    user.delete()
    assert TODO.objects.count() == 0
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_otp():
    client = APIClient()
    response = client.get(reverse('otp', kwargs={'uid': '1'}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile():
    user = User.objects.create_user(username='testuser', password='testpassword')
    profile = Profile.objects.create(user=user, phone_number='1234567890', otp=1234)

    assert profile.phone_number == '1234567890'    
    assert profile.otp == 1234
    assert profile.user == user
    assert profile.uid is not None
    assert isinstance(profile.uid, uuid.UUID)
    assert Profile.objects.filter(uid=profile.uid).count() == 1
    assert profile._meta.get_field('uid').editable is False
    assert Profile.objects.filter(phone_number='1234567890').count() == 1
    assert profile.phone_number is not None
    assert profile.otp is not None
    assert isinstance(profile.otp, int)
    assert Profile.objects.filter(otp=1234).count() == 1
    
    profile.delete()
    user.delete()
    assert Profile.objects.count() == 0
    assert User.objects.count() == 0



@pytest.mark.usefixtures('db') #usefixtures is used to tell pytest to use the database
def test_TODO():
    user = User.objects.create_user(username='testuser', password='testpassword')
    todo = TODO.objects.create(title='Test TODO', user=user, status='Pending')
    
    assert todo.title == 'Test TODO'
    assert todo.status == 'Pending'
    assert todo.user == user
    assert todo.date is not None
    assert isinstance(todo.date, datetime.datetime) #this will check if the date is in datetime format
    assert todo.status is not None
    assert todo.title is not None
    assert isinstance(todo.title, str)
    assert todo.user is not None
    assert isinstance(todo.user, User)
    assert todo.user == user
    assert str(todo) == 'Test TODO'
    todo.delete()
    assert TODO.objects.filter(id=todo.id).count() == 0

    todo = TODO.objects.create(title='Test TODO', user=user, status='Pending')
    todo.status = 'Completed'
    todo.save()
    assert TODO.objects.get(id=todo.id).status == 'Completed'
    assert TODO.objects.get(id=todo.id) == todo
    assert TODO.objects.filter(title='Test TODO').count() == 1 #this will check if the todo with title 'Test TODO' exists
    assert TODO.objects.count() == 1 
    
    todo.delete()
    user.delete()
    assert TODO.objects.count() == 0
    assert User.objects.count() == 0


    
@pytest.mark.django_db
def test_view_todo():
    user = User.objects.create_user(username='testuser', password='testpassword')
    todo = TODO.objects.create(title='Test TODO', user=user, status='Pending')
    client = APIClient()
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('view_todo', kwargs={'id': todo.id}))
    assert response.status_code == 200
    assert response.data['title'] == 'Test TODO'
    assert response.data['status'] == 'Pending'
    assert response.data['user'] == user.id
    assert response.data['date'] is not None
    
    todo.delete()
    user.delete()
    assert TODO.objects.count() == 0
    assert User.objects.count() == 0
    assert Profile.objects.count() == 0



  