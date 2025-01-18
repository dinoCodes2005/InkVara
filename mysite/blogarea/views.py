from multiprocessing import context
from unicodedata import category
from urllib import response
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import logout,authenticate
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect

# Create your views here.
class BlogHome(ListView):
    model = Post
    template_name = 'blogHome.html'
    ordering = ['post_date']
    
class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_Detail.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post,id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        context['total_likes'] = total_likes
        return context       
        
class AddPostView(CreateView):
    model = Post
    template_name = 'writeBlog.html'
    fields = '__all__'
    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return redirect(self.object.get_absolute_url())

def LikeView(request,pk):
    post = get_object_or_404(Post,id=pk)
    if request.user in post.like.all():
        post.like.remove(request.user)  # Unlike the post
        
    else:
        post.like.add(request.user) 
    return HttpResponseRedirect(reverse('ArticleDetailView',args=[pk]))
    
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

