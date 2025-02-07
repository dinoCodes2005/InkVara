from ast import mod
from os import name
from tabnanny import verbose
from tkinter import CASCADE
from turtle import position
from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime,date
from ckeditor.fields import RichTextField

# Create your models here.
# class Hashtag(models.Model):
#     name = models.CharField(max_length=50,unique=True)
    
#     def __str__(self):
#          return '#'+self.name
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
    category = models.CharField(choices=choices,max_length=255,default="Uncategorized")
    articleSnippet = models.CharField(max_length=150,default="Default Article Snippet")
    thumbnail = models.ImageField(upload_to='thumbnail/',null=True,blank=True)
    like = models.ManyToManyField(User,related_name='blog_posts',null=True,blank=True)
    body = RichTextField(blank=True,null=True)
    
    def total_likes(self):
        return self.like.count()

    def __str__(self):
        return self.title + ' | ' +  str(self.author)

    def get_absolute_url(self):
            return reverse('ArticleDetailView', args=[self.id])

class Profile(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    bio = models.TextField()
    profileImage = models.ImageField(upload_to='profile_pics',null=True,blank=True)
    profileBackground = models.ImageField(upload_to='profile_background',null=True,blank=True)
    twitter_link = models.URLField(max_length=200,null=True,blank=True,default="https://x.com/")
    instagram_link = models.URLField(max_length=200,null=True,blank=True,default="https://instagram.com/")
    youtube_link = models.URLField(max_length=200,null=True,blank=True,default="https://youtube.com/")
    location = models.CharField(max_length=150,null=True,blank=True,default="Earth")
    occupation = models.CharField(max_length=50,null=True,blank=True,default="Occupation")
    industry = models.CharField(max_length=50,null=True,blank=True,default="Industry")
    position = models.CharField(max_length=50,null=True,blank=True,default="position")

    def __str__(self):
        return str(self.user)

