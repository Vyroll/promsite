from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.utils import timezone
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.db import transaction
from django.forms import formset_factory
import datetime

from .models import Post, Comment
from .forms import PostForm, CommentForm, PostFilter

import logging
logger = logging.getLogger(__name__)

class RedirectMixin(AccessMixin):
    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(message)
        return redirect_to_login(
            self.request.get_full_path(),
            self.get_login_url(),
            self.get_redirect_field_name()
        )

# List Posts
class IndexView(View):
    """List all Posts"""
    template_name = 'blogdemo/post/index.html'

    def get(self, request, *args, **kwargs):
        post_list = Post.objects.all()
        post_filter = PostFilter(request.GET, queryset=post_list)
        
        return render(request, self.template_name, {'posts':post_list, 'filter':post_filter})

class DetailView(View):
    """Detail Post view"""
    template_name = 'blogdemo/post/detail.html'
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        post = Post.objects.get(pk=kwargs['pk'])
        comments = Comment.objects.filter(post=post.id)

        return render(request, self.template_name, {'post':post, 'comments':comments, 'form':form})
        
    def test_func(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return post.creator.id == self.request.user.id
        
class CreatePostView(LoginRequiredMixin, View):
    """Creating Post"""
    template_name = 'blogdemo/post/create_post.html'
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

class EditPostView(RedirectMixin, UserPassesTestMixin, View):
    """Edit Post"""
    template_name = 'blogdemo/post/post_edit.html'
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        form = self.form_class(instance=post)

        return render(request, self.template_name, {'form': form, 'post_id':kwargs['pk']})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)

        if form.is_valid():
            post = Post.objects.get(pk=kwargs['pk'])
            fields = {}
            for key, value in form.cleaned_data.items():
                fields[key]=value
                
            post.title = fields['title']
            post.text = fields['text']

            try:
                post.save()
            except IntegrityError as e:
                messages.error(request, "Something went wrong while saving")
                messages.debug(request, f'{e.__cause__}')
            else:
                messages.success(request, "Your changes have been saved!")
        else:
            messages.error(request, "Something went wrong, your post wasn't created!")
        return render(request, self.template_name, {'form': form, 'post_id':kwargs['pk']})
        
    def test_func(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return post.creator.id == self.request.user.id

class CreateCommentView(LoginRequiredMixin, View):
    """Creating Comment"""
    template_name = 'blogdemo/post/detail.html'
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
                messages.error(request, "Something went wrong while saving")
                messages.debug(request, f'{e.__cause__}')
            else:
                messages.success(request, "Your comment have been saved!")
        else:
            messages.error(request, "Something went wrong, your comment wasn't created!")

        return render(request, self.template_name, {'post':post, 'comments':comments, 'form':form})
        
class DeletePostView(RedirectMixin, UserPassesTestMixin, View):
    """Delete Post"""

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        
        try:
            post.delete()
        except IntegrityError as e:
            messages.error(request, "Something went wrong while deleting post")
            messages.debug(request, f'{e.__cause__}')
        else:
            messages.success(request, "Post has been deleted!")
        
        return HttpResponseRedirect(reverse('blogdemo:profile'))
        
    def test_func(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return post.creator.id == self.request.user.id

class ProfileView(LoginRequiredMixin, View):
    template_name = 'blogdemo/profile.html'
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().filter(creator=request.user.id)
        return render(request, self.template_name, {'posts':posts})
        
class OwnerAccessView(LoginRequiredMixin, View):
    template_name = 'blogdemo/showcase/owner_access.html'
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        return render(request, self.template_name, {'posts':posts})
        
class TransactionsView(LoginRequiredMixin, View):
    template_name = 'blogdemo/showcase/transactions.html'
    PostFormSet = formset_factory(PostForm)
    CommentFormSet = formset_factory(CommentForm)
    
    def get(self, request, *args, **kwargs):
        post_formset = self.PostFormSet(prefix='posts')
        comment_formset = self.CommentFormSet(prefix='comments')
        
        recent = timezone.now() - datetime.timedelta(hours=2)
        posts = Post.objects.all().filter(pub_date__gte=recent)
        comments = Comment.objects.all().filter(pub_date__gte=recent)

        return render(request, self.template_name, {
            'post_formset':post_formset,
            'comment_formset':comment_formset,
            'posts':posts,
            'comments':comments,
            })

    # @transaction.atomic
    def post(self, request, *args, **kwargs):
        post_formset = self.PostFormSet(request.POST, prefix='posts')
        comment_formset = self.CommentFormSet(request.POST, prefix='comments')

        if post_formset.is_valid() and comment_formset.is_valid():
            messages.success(request, "form is valid")
            try:
                # with transaction.atomic():
                    post = Post.objects.create(
                        title=post_formset[0].cleaned_data['title'],
                        text=post_formset[0].cleaned_data['text'],
                        pub_date=timezone.now(),
                        creator=request.user,
                    )
                    for form in comment_formset:
                        Comment.objects.create(
                            post=post,
                            creator=request.user,
                            # pub_date=timezone.now(),
                            text=form.cleaned_data["text"],
                        )
            except IntegrityError:
                messages.error(request, "Smth went wrong")
        else:
            messages.error(request, "form is not valid")
            
        return HttpResponseRedirect(reverse('blogdemo:transactions'))
        
class TransactionsSafeView(View):
    template_name = 'blogdemo/showcase/transactions.html'
    PostFormSet = formset_factory(PostForm)
    CommentFormSet = formset_factory(CommentForm)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        post_formset = self.PostFormSet(request.POST, prefix='posts')
        comment_formset = self.CommentFormSet(request.POST, prefix='comments')

        if post_formset.is_valid() and comment_formset.is_valid():
            messages.success(request, "form is valid")
            try:
                with transaction.atomic():
                    post = Post.objects.create(
                        title=post_formset[0].cleaned_data['title'],
                        text=post_formset[0].cleaned_data['text'],
                        pub_date=timezone.now(),
                        creator=request.user,
                    )
                    for form in comment_formset:
                        Comment.objects.create(
                            post=post,
                            creator=request.user,
                            # pub_date=timezone.now(),
                            text=form.cleaned_data["text"],
                        )
            except IntegrityError:
                messages.error(request, "Smth went wrong")
        else:
            messages.error(request, "form is not valid")
            
        return HttpResponseRedirect(reverse('blogdemo:transactions'))

class ApiAuthorisationView(View):
    template_name = 'blogdemo/showcase/api_authorisation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
