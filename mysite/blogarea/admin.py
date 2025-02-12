from django.contrib import admin
from .models import   Comment, Post,Category, Profile
# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)
