from profile import Profile
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from .forms import ProfileEditForm, UserRegisterForm
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import *\

# Create your views here.
class UserRegisterView(generic.CreateView):
    form_class = UserRegisterForm
    template_name = 'signUp.html'
    success_url = reverse_lazy('login')
    
class EditProfileView(generic.UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'registration/editProfile.html'
    success_url = reverse_lazy('blogarea') 

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        response = super().form_valid(form)
        return response
    
def login_home(request):
    return render(request,'registration/login.html')

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


