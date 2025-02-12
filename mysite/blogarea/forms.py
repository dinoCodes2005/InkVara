from cProfile import label

from click import style

from core import models
from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {'body':'Comment'}
        widgets = {
            'body' : forms.Textarea(attrs={'placeholder':'Comment Here !!',
                                           'id':'comment-text',
                                           'rows':10,
                                           'cols':50,
                                           'style':'width:80%;height:150px;',})
        }