from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import User
from .models import *

# Create your views here.

def login_home(request):
    return render(request,'login.html')

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request,'Your Username is incorrect or this account doesn\'t exist. ')
            return render(request,'login.html',{'hasFailedAuthentication':True})

        user = authenticate(username=username,password=password)

        if user is None:
            messages.error(request,"Your Password is incorrect or this account doesn\'t exist. ")
            return render(request,'login.html',{'hasFailedAuthentication':True})
        else:
            login(request,user)
            return redirect('blogarea')
    else:
        return render(request, 'login.html',{'hasFailedAuthentication':False})

def signUp_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return render(request,'login.html',{'hasFailedAuthentication':False})
    else:
        form = UserRegisterForm()
    return render(request,'signUp.html',{'form':form})

def blogarea(request):
    return render(request,'blogHome.html')


