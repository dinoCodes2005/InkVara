from multiprocessing import context
import random
from sre_constants import SUCCESS
from unicodedata import category
from urllib import request, response
from wsgiref.util import request_uri
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import logout,authenticate 
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from requests import post
from .models import Category, Comment, Hashtag, Post, Profile
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect , StreamingHttpResponse
from django.db.models import Count,Q
from blogarea.models import Profile
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CommentForm, PostForm
from django.views.generic.edit import FormMixin
from openai import OpenAI
import google.generativeai as genai
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Post, Hashtag
from .forms import PostForm
from django.conf import settings
# Create your views here.
class BlogHome(ListView):
    model = Post
    template_name = 'blogHome.html'
    ordering = ['post_date']
    
    def get_context_data(self, **kwargs):
        context = super(BlogHome, self).get_context_data(**kwargs)
        #annotate is used to add extra field to each object without saving it to databse just for sorting or calculation purposes
        posts = Post.objects.annotate(like_count=Count('like')).order_by('-like_count')
        
        post_with_highest_likes = posts.first()  # The post with the highest likes
        post_with_second_highest_likes = posts[1] if len(posts) > 1 else None  # The second post, if it exists
        post_with_third_highest_likes = posts[2] if len(posts) > 2 else None  # The third post, if it exists
        post_with_fourth_highest_likes = posts[3] if len(posts) > 3 else None  # The fourth post, if it exists
        non_featured_post = posts.exclude(id__in=[post_with_highest_likes.id,
                                                  post_with_second_highest_likes.id,
                                                  post_with_third_highest_likes.id,
                                                  post_with_fourth_highest_likes.id,]
                                          )

    # Add posts to context
        context['posts'] = non_featured_post[:9]
        context['post_with_highest_likes'] = post_with_highest_likes
        context['post_with_second_highest_likes'] = post_with_second_highest_likes
        context['post_with_third_highest_likes'] = post_with_third_highest_likes
        context['post_with_fourth_highest_likes'] = post_with_fourth_highest_likes
    
        return context
    
class ArticleDetailView(DetailView,FormMixin):
    model = Post
    template_name = 'article_Detail.html'
    form_class = CommentForm
    
    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        posts = Post.objects.annotate(like_count=Count('like')).order_by('-like_count')
        current_post = get_object_or_404(Post,id=self.kwargs['pk'])
        related_posts = posts.filter(Q(category=current_post.category) | Q(tags__tag__in=current_post.tags.all()) ).exclude(id=current_post.id)
        total_words = current_post.word_count()
        total_likes = current_post.total_likes()
        has_liked = self.request.user in current_post.like.all() if self.request.user.is_authenticated else False 
        comments = Comment.objects.filter(post_id = current_post.id)
        comments_number = comments.count()
            
        context['current_post'] = current_post
        context['comments_number'] = comments_number
        context['comments'] =  list(comments.filter(user=self.request.user)) + list(comments.exclude(user=self.request.user).order_by('-comment_date')) if self.request.user.is_authenticated else list(comments)
        context['form'] = self.get_form()
        context['has_liked'] = has_liked
        context['related_posts'] = related_posts[:4]
        context['posts'] = posts
        context['total_likes'] = total_likes
        context['total_words'] = total_words
        return context       
    
    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object 
            comment.user = self.request.user
            comment.save()
            return redirect('ArticleDetailView',pk=self.object.pk)
        return self.form_invalid(form) 
    
class ShowProfileView(DetailView):
    model = Profile
    template_name = 'showProfilePage.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfileView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile,id=self.kwargs['pk'])
        posts = Post.objects.filter(author = page_user.user).order_by('-post_date')
        total_posts = Post.objects.filter(author=page_user.user).count()
        total_likes = Post.objects.filter(author=page_user.user).aggregate(total_likes=Count('like'))['total_likes'] or 0
        skills = page_user.skills.split(',') if page_user.skills else []
        education = page_user.education.split(',') if page_user.education else []
        show_load_more = True
        if posts.count()<4:
            show_load_more = False
        context['show_load_more'] = show_load_more
        context['posts'] = posts[:4]
        context['education'] = education
        context['skills'] = skills
        context['page_user'] = page_user
        context['total_posts'] = total_posts
        context['total_likes'] = total_likes
        
        return context    

class AddPostView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = 'writeBlog.html'
    form_class = PostForm
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        
        # Process hashtags
        tags = form.instance.hashtags
        tags_list = [tag.strip().lstrip('#') for tag in tags.split(',') if tag.strip()]
        
        for tag in tags_list:
            hashtag, created = Hashtag.objects.get_or_create(tag=tag)
            hashtag.post.add(form.instance)
            form.instance.tags.add(hashtag)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('ArticleDetailView', kwargs={'pk': self.object.pk})

def CategoryView(request,tag):
    category_posts = Post.objects.filter(Q(tags__tag = tag) | Q(category = tag)).distinct()
    return render(request,'categories.html',{'posts':category_posts,'category':tag})

class CategoriesView(ListView):
    model = Hashtag
    template_name = "categoriesPage.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all()
        context["categories"] = Category.objects.all()
        return context
    
@login_required
def UpdatePostView(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            #creating the object temporarily for manipulation
            post = form.save(commit=False) 
            post.tags.clear()
            
            if post.hashtags:
                tags_list = [tag.strip().lstrip('#') for tag in post.hashtags.split(',') if tag.strip()]
                for tag in tags_list:
                    hashtag, created = Hashtag.objects.get_or_create(tag=tag)
                    hashtag.post.add(post)
                    post.tags.add(hashtag)
                    
            #saving the object to DB after doing the manipulation
            post.save()
            messages.success(request, "Post has been updated successfully!")
            return redirect(reverse('ArticleDetailView', kwargs={'pk': post.pk}))
        else:
            messages.error(request, "There was an error in saving the post!")

    else:
        form = PostForm(instance=post)

    return render(request, 'updateBlog.html', {'form': form})

@login_required
def deleteBlog(request,pk):
    post = Post.objects.get(id=pk)
    if request.method == "POST":
        post.delete()
        messages.success(request,"Post has been deleted successfully !!")
        return redirect("blogarea")
    return redirect(reverse_lazy("blogarea"))

def logout_user(request):
    logout(request)
    messages.success(request,"You have logged out")
    return redirect('home')

def load_more(request):
    offset=int(request.POST.get('offset',False))
    limit=6
    posts=Post.objects.all()[offset:limit+offset]
        
    post_list = [
        {
            "id":post.id,
            "title":post.title,
            "articleSnippet":post.articleSnippet,
            "post_date":post.post_date,
            "thumbnail":request.build_absolute_uri(post.thumbnail.url)
                    if post.thumbnail
                    else 
                    request.build_absolute_uri('/media/thumbnail/thumbnail.jpg'),    
            "author":{
                "id":post.author.id,
                "username":post.author.username,
                "profile":{
                    "profile-id":post.author.profile.id,
                    "profileImage": request.build_absolute_uri(post.author.profile.profileImage.url)
                    if post.author.profile.profileImage
                    else 
                    request.build_absolute_uri('/media/thumbnail/thumbnail.jpg') ,
                }
            }
        }
        for post in posts
    ]
    
    totalData=Post.objects.count()
    return JsonResponse(data={
        'posts':post_list[:3],
        'totalResult':totalData,

    })

def filtered_load_more(request):
    offset=int(request.POST.get('offset',False))
    filter = request.POST.get('filter',False)
    limit=6
    posts=Post.objects.filter(author_id = filter )[offset:limit+offset]
    post_list = [
        {
            "id":post.id,
            "title":post.title,
            "articleSnippet":post.articleSnippet,
            "post_date":post.post_date,
            "thumbnail":request.build_absolute_uri(post.thumbnail.url)
                    if post.thumbnail
                    else 
                    request.build_absolute_uri('/media/thumbnail/thumbnail.jpg'),    
            "author":{
                "id":post.author.id,
                "username":post.author.username,
                "profile":{
                    "profile-id":post.author.profile.id,
                    "profileImage": request.build_absolute_uri(post.author.profile.profileImage.url)
                    if post.author.profile.profileImage
                    else 
                    request.build_absolute_uri('/media/thumbnail/thumbnail.jpg') ,
                }
            }
        }
        for post in posts
    ]
        
    totalData=Post.objects.filter(author_id = filter).count()
    return JsonResponse(data={
        'posts':post_list,
        'totalResult':totalData,
    })

@login_required   
def submit_comment(request):
    if request.method == 'POST':
        body = request.POST.get('body')
        user = request.user
        post_id = request.POST.get('post')
        if body and user.is_authenticated:
            post = Post.objects.get(id = post_id)
            comment = Comment.objects.create(user = user,body = body,post = post)    
            return JsonResponse({
                'success' : True,
                'comment' : {
                    'id':comment.id,
                    'user':comment.user.username,
                    'body':comment.body,
                    'comment_date':comment.comment_date,
                    'profile_image': request.build_absolute_uri(comment.user.profile.profileImage.url)
                    if comment.user.profile.profileImage 
                    else 
                    request.build_absolute_uri('/media/thumbnail/thumbnail.jpg') ,
                    'profile_url':f"/show_profile_page/{comment.user.profile.id}/",
                    'comment_likes':0,
                    'comment_dislikes':0,
                }
            })
        return JsonResponse({
            'success':False,
            'error':"not authenticated / invalid data"
        })
    return JsonResponse({
        'success':False,
        'error':'Invalid Request Method'
    })

@login_required
def LikeView(request,pk):
    if request.method == "POST":
        post_id = request.POST.get('post_id',False)
        post = Post.objects.get(id = post_id)
        liked = False
        if request.user.is_authenticated:
            if request.user in post.like.all():
                post.like.remove(request.user)                   # Unlike the post
            else:
                post.like.add(request.user) 
                liked = True
        return JsonResponse(data={
        'success':True,
        'liked':liked,
        'likes':post.total_likes(),
    })
    else:
        return JsonResponse(data={
            'success':False,
        })

genai.configure(api_key= settings.GEMINI_API_KEY)
          
def generate_response(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt, stream=True)  

    def stream_data():
        try:
            for chunk in response:
                if chunk.text:
                    yield chunk.text + " "  
        except Exception as e:
            yield f"Error: {str(e)}"

    return StreamingHttpResponse(stream_data(), content_type="text/plain")

@csrf_exempt
def answer(request):   
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt", "No prompt provided")
            return generate_response(prompt) 
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
def searchresult(request):
    if request.method == "GET":
        data = request.GET.get("q","")
        
        posts = Post.objects.filter(Q(title__icontains=data) | 
                    Q(tags__tag__icontains=data) | 
                    Q(author__username__icontains=data)).distinct()
        if not posts:
            return render(request,"searchresult.html",{"posts":Post.objects.all()[:5],"found":0,"values":str(data)})

        return render(request,"searchresult.html",{"posts":posts,"values":str(data),"found":1})
    else:   
        return JsonResponse({"error":"Not a GET request"})


def search(request):
    if request.method == "GET":
        data = request.GET.get("title","")
        if not data:
            return random_post(request)
        
        posts = list(Post.objects.filter(
                    Q(title__icontains=data) | 
                    Q(tags__tag__icontains=data) | 
                    Q(author__username__icontains=data))
                    .values("title", "id", "author__username").distinct()[:5])

        return JsonResponse({"posts":posts})
    else:   
        return JsonResponse({"error":"Not a GET request"})
    
def random_post(request):
    if request.method == "GET":
        posts = list(Post.objects.order_by("-like")[:5].values("title","id","author__username"))
        return JsonResponse({"posts":posts})
    else:   
        return JsonResponse({"error":"Not a GET request"})
            
        
        