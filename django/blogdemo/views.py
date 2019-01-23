from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.utils import timezone
from django.contrib import messages
from django.db import IntegrityError

from .models import Post, Comment
from .forms import PostForm, CommentForm, PostFilter

import logging
logger = logging.getLogger(__name__)

# List Posts
class IndexView(View):
    """List all Posts"""
    template_name = 'blogdemo/index.html'

    def get(self, request, *args, **kwargs):
        post_list = Post.objects.all()
        post_filter = PostFilter(request.GET, queryset=post_list)
        
        return render(request, self.template_name, {'posts':post_list, 'filter':post_filter})

class DetailView(View):
    """Detail Post view"""
    template_name = 'blogdemo/detail.html'
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        post = Post.objects.get(pk=kwargs['pk'])
        comments = Comment.objects.filter(post=post.id)

        return render(request, self.template_name, {'post':post, 'comments':comments, 'form':form})
        
class CreatePostView(View):
    """Creating Post"""
    template_name = 'blogdemo/create_post.html'
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)

        if form.is_valid():
            fields = {}
            for key, value in form.cleaned_data.items():
                fields[key]=value
            fields['creator']=request.user
            fields['pub_date']=timezone.now()
            post = Post(**fields)

            try:
                post.save()
            except IntegrityError as e:
                messages.error(request, "smthing went wrong while saving")
                messages.debug(request, f'{e.__cause__}')
            else:
                messages.success(request, "Your post have been saved!", "alert alert-success")

            return HttpResponseRedirect(reverse('blogdemo:index'))
        else:
            messages.error(request, "Something went wrong, your post wasn't created!")

            return render(request, self.template_name, {'form': form})
            
class CreateCommentView(View):
    """Creating Comment"""
    template_name = 'blogdemo/detail.html'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        post = Post.objects.get(pk=kwargs['pk'])
        comments = Comment.objects.filter(post=post.id)

        if form.is_valid():
            fields = {}
            for key, value in form.cleaned_data.items():
                fields[key]=value
            fields['creator']=request.user
            fields['post_id']=kwargs['pk']
            
            fields['pub_date']=timezone.now()
            comment = Comment(**fields)

            try:
                comment.save()
            except IntegrityError as e:
                messages.error(request, "smthing went wrong while saving")
                messages.debug(request, f'{e.__cause__}')
            else:
                messages.success(request, "Your comment have been saved!", "alert alert-success")

            return render(request, self.template_name, {'post':post, 'comments':comments, 'form':form})
        else:
            messages.error(request, "Something went wrong, your comment wasn't created!")
            
            return render(request, self.template_name, {'post':post, 'comments':comments, 'form':form})

class ProfileView(View):
    template_name = 'blogdemo/profile.html'
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().filter(creator=request.user.id)
        return render(request, self.template_name, {'posts':posts})