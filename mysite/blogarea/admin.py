from django.contrib import admin
from .models import   Comment, Hashtag, Post,Category, Profile, Reply
# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Hashtag)
