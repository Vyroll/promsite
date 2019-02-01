from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth import login, authenticate
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.urls import reverse

class SignupView(View):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            # create user
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=raw_password)

            # redirect
            if user is not None:
                messages.success(request, "You have successfully created your account!")
                login(request, user)
                return HttpResponseRedirect(reverse('blogdemo:index'))
            else:
                messages.error(request, "Somethink went wrong, your account wasn't created.")
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})