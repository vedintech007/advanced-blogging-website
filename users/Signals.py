from django.db.models.signals import post_save, pre_delete
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.signals import (
    user_logged_in, user_logged_out, user_login_failed)
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    if user:
        msg = f'You signed out {request.user.username}!'
    else:
        msg = 'You signed out!'

    messages.add_message(request, messages.SUCCESS, msg)


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    if user:
        msg = f'Signed in as {request.user.username}!'
    else:
        msg = f'Signed in!'

    messages.add_message(request, messages.SUCCESS, msg)


@receiver(user_login_failed)
def on_user_logged_in_failed(sender, request, user, **kwargs):
    if user:
        msg = 'Sign in failed!'
    else:
        msg = 'Sign in failed!'

    messages.add_message(request, messages.ERROR, msg)
