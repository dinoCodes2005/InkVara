from unicodedata import category
from django.shortcuts import render,redirect
from django.contrib.auth import logout,authenticate
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.urls import reverse_lazy
# Create your views here.
class BlogHome(ListView):
    model = Post
    template_name = 'blogHome.html'
    ordering = ['post_date']
    
class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_Detail.html'

class AddPostView(CreateView):
    model = Post
    template_name = 'writeBlog.html'
    fields = '__all__'

class UpdatePostView(UpdateView):
    model = Post
    template_name = 'updateBlog.html'
    fields = ['title','category','thumbnail','body']

class DeletePostView(DeleteView):
    model = Post
    template_name = 'deleteBlog.html'
    success_url = reverse_lazy('blogarea')

def logout_user(request):
    logout(request)
    messages.success(request,"You have logged out")
    return redirect('home')

def CategoryView(request,cats):
    category_name = cats.replace('-',' ').title()
    category_posts = Post.objects.filter(category=category_name)
    return render(request,'categories.html',{'category_posts':category_posts})

