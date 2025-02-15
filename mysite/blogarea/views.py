from multiprocessing import context
from sre_constants import SUCCESS
from unicodedata import category
from urllib import request, response
from wsgiref.util import request_uri
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import logout,authenticate
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from requests import post
from .models import Comment, Post, Profile
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
from django.db.models import Count
from blogarea.models import Profile
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CommentForm
from django.views.generic.edit import FormMixin
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
        related_posts = posts.filter(category=current_post.category).exclude(id=current_post.id)
        total_words = current_post.word_count()
        total_likes = current_post.total_likes()
        has_liked = self.request.user in current_post.like.all() if self.request.user.is_authenticated else False 
        comments = Comment.objects.filter(post_id = current_post.id)
        comments_number = comments.count()
        context['current_post'] = current_post
        context['comments_number'] = comments_number
        context['comments'] = list(comments.filter(user=self.request.user)) + list(comments.exclude(user=self.request.user).order_by('-comment_date'))
        context['form'] = self.get_form()
        context['has_liked'] = has_liked
        context['related_posts'] = related_posts
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
        context['posts'] = posts[:4]
        context['education'] = education
        context['skills'] = skills
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
        'posts':post_list,
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
    
def submit_comment(request):
    if request.method == 'POST':
        body = request.POST.get('body')
        user = request.user
        post_id = request.POST.get('post')
        if body and user.is_authenticated:
            post = Post.objects.get(id = post_id)
            comment = Comment.objects.create(user = user,body = body,post = post)
            
            if comment.user.profile.profileImage:
                profile_image = request.build_absolute_uri(comment.user.profile.profileImage.url)
            else:
                profile_image = request.build_absolute_uri('/media/thumbnail/thumbnail.jpg')
            return JsonResponse({
                'success' : True,
                'comment' : {
                    'user':comment.user.username,
                    'body':comment.body,
                    'comment_date':comment.comment_date,
                    'profile_image':profile_image,
                    'profile_url':f"/show_profile_page/{comment.user.profile.id}/",
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