from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/blogPostImages/',null=True,blank=True)
    thumbnail = models.ImageField(upload_to='thumbnail/',null=True,blank=True)
    body = models.TextField()

    # def __str__(self):
    #     return self.title + '|' +  str(self.author)

    def get_absolute_url(self):
        return reverse('ArticleDetailView',args=(str(self.id)))


