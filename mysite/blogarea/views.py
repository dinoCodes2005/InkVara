from multiprocessing import context
from unicodedata import category
from urllib import response
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import logout,authenticate
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Profile
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
from django.db.models import Count
from blogarea.models import Profile
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
class BlogHome(ListView):
    model = Post
    template_name = 'blogHome.html'
    ordering = ['post_date']
    
    def get_context_data(self, **kwargs):
        context = super(BlogHome, self).get_context_data(**kwargs)
        posts = Post.objects.annotate(like_count=Count('like')).order_by('-like_count')
        post_with_highest_likes = posts.first()  # The post with the highest likes
        post_with_second_highest_likes = posts[1] if len(posts) > 1 else None  # The second post, if it exists
        post_with_third_highest_likes = posts[2] if len(posts) > 2 else None  # The third post, if it exists
        post_with_fourth_highest_likes = posts[3] if len(posts) > 3 else None  # The fourth post, if it exists

    # Add posts to context
        context['posts'] = posts[:8]
        context['post_with_highest_likes'] = post_with_highest_likes
        context['post_with_second_highest_likes'] = post_with_second_highest_likes
        context['post_with_third_highest_likes'] = post_with_third_highest_likes
        context['post_with_fourth_highest_likes'] = post_with_fourth_highest_likes
    
        return context
    
class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_Detail.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post,id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        context['total_likes'] = total_likes
        return context       
    
class ShowProfileView(DetailView):
    model = Profile
    template_name = 'showProfilePage.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfileView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile,id=self.kwargs['pk'])
        total_posts = Post.objects.filter(author=page_user.user).count()
        total_likes = Post.objects.filter(author=page_user.user).aggregate(total_likes=Count('like'))['total_likes'] or 0
        context['page_user'] = page_user
        context['total_posts'] = total_posts
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
    fields = ['title','articleSnippet','category','thumbnail','body']

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

def load_more(request):
    offset=int(request.POST['offset'])
    limit=6
    posts=Post.objects.all()[offset:limit+offset]
    totalData=Post.objects.count()
    data={}
    posts_json=serializers.serialize('json',posts)
    return JsonResponse(data={
        'posts':posts_json,
        'totalResult':totalData
    })