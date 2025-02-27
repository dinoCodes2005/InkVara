from ast import mod
from os import name, truncate
from tabnanny import verbose
from tkinter import CASCADE
from turtle import position
from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime,date
from ckeditor.fields import RichTextField
from django.utils.html import strip_tags
from phonenumber_field.modelfields import PhoneNumberField
from requests import post

class Category(models.Model):
    name = models.CharField(max_length=255,default="Uncategorized")
    
    def __str__(self):
        return self.name
    
    def get_absoulte_url(self):
        return reverse('ArticleDetailView', args=[self.id])
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Post(models.Model):
    
    choices = Category.objects.all().values_list('name','name')
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    post_date = models.DateField(auto_now_add=True)
    hashtags = models.TextField(max_length=200,null=True)
    category = models.CharField(choices=choices,max_length=255,default="Uncategorized")
    articleSnippet = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to='thumbnail/',null=True,blank=True, default='thumbnail/thumbnail.jpg')
    like = models.ManyToManyField(User,related_name='blog_posts',null=True,blank=True)
    tags = models.ManyToManyField("Hashtag",related_name="posts",null=True,blank=True)
    body = RichTextField(blank=True,null=True)
    
    def total_likes(self):
        return self.like.count()
    
    def word_count(self):
        text_content = strip_tags(self.body)
        return len(text_content.split())

    def __str__(self):
        return self.title + ' | ' +  str(self.author)

    def get_absolute_url(self):
            return reverse('ArticleDetailView', args=[self.id])


class Profile(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    bio = models.TextField()
    blogcaption = models.CharField(max_length=150,null=True,blank=True,default="Former Adventurer turned full-time Dad moonlighting as an author")
    profileImage = models.ImageField(upload_to='profile_pics',null=True,blank=True)
    profileBackground = models.ImageField(upload_to='profile_background',null=True,blank=True)
    twitter_link = models.URLField(max_length=200,null=True,blank=True,default="https://x.com/")
    instagram_link = models.URLField(max_length=200,null=True,blank=True,default="https://instagram.com/")
    youtube_link = models.URLField(max_length=200,null=True,blank=True,default="https://youtube.com/")
    contact = PhoneNumberField(blank=True, null=True)
    location = models.CharField(max_length=150,null=True,blank=True,default="Earth")
    occupation = models.CharField(max_length=50,null=True,blank=True,default="Occupation")
    industry = models.CharField(max_length=50,null=True,blank=True,default="Industry")
    position = models.CharField(max_length=50,null=True,blank=True,default="position")
    skills = models.TextField(null=True,blank=True,help_text="Enter your skills separated by commas")
    education = models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.user)

class Comment(models.Model):
    post = models.ForeignKey(Post,null=True,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    body = models.TextField()
    comment_date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name='liked_comment',blank=True,default=0)
    dislikes = models.ManyToManyField(User,related_name='disliked_comment',blank=True)
    
    def __str__(self):
        return f"{self.post.title} - {self.user.username} - {self.body[:25]}"
    
    def total_likes(self):
        return self.likes.count()
    
    def total_dislikes(self):
        return self.dislikes.count()
    
class Reply(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,null=True,on_delete=models.CASCADE)
    body = models.TextField()
    reply_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name='liked_reply',blank=True)
    dislikes = models.ManyToManyField(User,related_name='disliked_reply',blank=True)
    
    def __str__(self):
        return f"{self.user} - {self.comment | truncate:20}"
    
    def total_likes(self):
        return self.likes.count()
    
    def total_dislikes(self):
        return self.dislikes.count()
    
class Hashtag(models.Model):
    tag = models.CharField(max_length = 20,null=True,blank=True)
    post = models.ManyToManyField(Post,null=True,related_name='hashtag_posts')
    
    def __str__(self):
        return self.tag
    
    def get_posts(self):
        return self.post.all()
    
    
    
    