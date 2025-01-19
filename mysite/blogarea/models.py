from ast import mod
from os import name
from tabnanny import verbose
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



