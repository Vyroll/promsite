from django.shortcuts import render
from django.views import View
from django.contrib import messages
from .models import Post, Comment

import logging

logger = logging.getLogger(__name__)

class IndexView(View):
    template_name = 'blogdemo/index.html'
    model = Post

    def get(self, request, *args, **kwargs):
        posts = self.model.objects.all()
        return render(request, self.template_name, {'posts':posts})

class DetailView(View):
    template_name = 'blogdemo/detail.html'
    model = Post

    def get(self, request, *args, **kwargs):
        post = self.model.objects.get(pk=kwargs['pk'])
        comments = Comment.objects.filter(post=post.id)

        return render(request, self.template_name, {'post':post, 'comments':comments})