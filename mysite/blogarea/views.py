from django.shortcuts import render,redirect
from django.contrib.auth import logout,authenticate
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from .models import Post
# Create your views here.
class BlogHome(ListView):
    model = Post
    template_name = 'blogHome.html'

class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_Detail.html'

class AddPostView(CreateView):
    model = Post
    template_name = 'writeBlog.html'
    fields = '__all__'

def logout_user(request):
    logout(request)
    messages.success(request,"You have logged out")
    return redirect('home')

