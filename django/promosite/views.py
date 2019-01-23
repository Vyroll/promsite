from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth import login, authenticate
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.urls import reverse

# TODO: SIGNALS
# https://docs.djangoproject.com/en/2.1/topics/signals/
# https://stackoverflow.com/questions/2719038/where-should-signal-handlers-live-in-a-django-project
# use signals to create messages when loges in and loges out

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
            
            # # add permisons
            # content_type = ContentType.objects.get_for_model(Question)
            # permission = Permission.objects.get(
            #     codename='view_question',
            #     content_type=content_type,
            # )
            # user.user_permissions.add(permission)
            
            # redirect
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully created your account!")
            else:
                messages.error(request, "Somethink went wrong, your account wasn't created.")

        return HttpResponseRedirect(reverse('blogdemo:index'))