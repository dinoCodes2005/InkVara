from django.contrib import admin
from .models import Hashtag, Post,Category
# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Hashtag)
