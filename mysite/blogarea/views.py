from unicodedata import category
from urllib import response
from django.shortcuts import render,redirect
from django.contrib.auth import logout,authenticate
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Hashtag, Post
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
    
    def form_valid(self, form):
        response =  super().form_valid(form)
        
        hashtags_str = self.request.POST.get('hashtags','')
        hashtags = [tag.strip() for tag in hashtags_str.split(',') if tag.strip()]
        tag_objects = []
        for tag in hashtags:
            tag_object ,created = Hashtag.objects.get_or_create(name=tag)
            tag_objects.append(tag_object)
        
        self.object.hashtags.set(tag_objects)

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

