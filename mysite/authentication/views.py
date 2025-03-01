from profile import Profile
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import ProfileEditForm, UserRegisterForm
from blogarea.models import Profile
from .forms import ProfileEditForm
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from blogarea.models import Profile
from django.contrib.auth.views import LoginView,LogoutView
from .models import *\



#redirecting to login page
def login_home(request):#
    return render(request,'registration/login.html')

#registering user
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'signUp.html', {'form': form})
    
@login_required
def edit_profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # Get or create profile instance

    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('blogarea')  # Redirect to the profile page or another relevant page
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'registration/editProfile.html', {'form': form})
    

class CustomLoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request,"Login successful !! Welcome Back")
        return super().form_valid(form)
    
class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request,"You have been logged out successfully !!")
        return super().dispatch(request, *args, **kwargs)


def blogarea(request):
    return render(request,'blogHome.html')


    


