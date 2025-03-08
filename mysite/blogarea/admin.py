from unicodedata import category
from django.contrib import admin
from .models import   Comment, Hashtag, Post,Category, Profile, Reply
# Register your models here.

admin.site.site_title = "Ink Vara"
admin.site.site_header = "Ink Vara Admin"

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author','post_date','category','articleSnippet','hashtags')
    search_fields = ('title','author','category')
    def change_category_to_default(self,request,queryset):
        queryset.update(category="News")
        
    actions = ('change_category_to_default',)

    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user__username','post__title','comment_date')
    search_fields = ('user__username','post__title')
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user__username','blogcaption')
    search_fields = ('user__username',)

admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Reply)
admin.site.register(Hashtag)
