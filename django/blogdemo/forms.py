from django import forms

from .models import Post

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import Textarea

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text',]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        labels={
            'text':''
        }
        widgets = {
            'text': Textarea(attrs={'rows': 3}),
        }
import django_filters
from django.db import models

class PostFilter(django_filters.FilterSet):
    creator = django_filters.CharFilter(lookup_expr='username__exact')
    class Meta:
        model = Post
        fields = ['creator',]