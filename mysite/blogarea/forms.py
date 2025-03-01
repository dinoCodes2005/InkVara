from cProfile import label

from click import style
import widget_tweaks

from core import models
from .models import Comment,Post
from django import forms
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {'body':'Comment'}
        widgets = {
            'body' : forms.Textarea(attrs={'placeholder':'Comment Here !!',
                                           'id':'comment-text',
                                           'rows':5,
                                           'cols':50,
                                           'style':' ',})
        }


class PostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())  

    class Meta:
        model = Post
        fields = ['title', 'hashtags', 'category', 'articleSnippet', 'thumbnail', 'body']
        labels = {
            'title': 'Title',
            'hashtags': 'Hashtags',
            'category': 'Category',
            'articleSnippet': 'Article Snippet',
            'thumbnail': 'Thumbnail',
            'body': 'Body',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter your post title...',
                'id': 'title',
                'class': 'form-control'
            }),
            'hashtag_text': forms.TextInput(attrs={
                'placeholder': 'Enter hashtags separated by commas. eg: #dance,#song,#games',
                'id': 'hashtags',
                'class': 'form-control'
            }),
            'articleSnippet': forms.TextInput(attrs={
                'placeholder': 'Enter your short snippet of Article Snippet..',
                'id': 'articleSnippet',
                'class': 'form-control'
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                'id': 'thumbnail',
                'class': 'form-control'
            }),
        }