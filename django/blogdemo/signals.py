from django.contrib.auth.signals import user_logged_out, user_logged_in,user_login_failed
from django.dispatch import receiver
from django.contrib import messages

@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.info(request, 'Logged out.')
    
@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    messages.success(request, 'You have successfully loged in!')
    
@receiver(user_login_failed)
def on_user_login_failed(sender, request, **kwargs):
    messages.error(request, 'Somethink went wrong. Please try again')