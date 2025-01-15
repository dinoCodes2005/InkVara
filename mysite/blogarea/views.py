from django.shortcuts import render,redirect
from django.contrib.auth import logout,authenticate
from django.contrib import messages
# Create your views here.
def blogarea(request):
    return render(request,'blogHome.html')

def logout_user(request):
    logout(request)
    messages.success(request,"You have logged out")
    return redirect('home')
