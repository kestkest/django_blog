from __future__ import absolute_import

from celery import shared_task, task

from django.contrib.auth import get_user_model

# User = get_user_model()

from core.models import User


@shared_task
def send_activation_mail(user_id, confirm_url):
    user = User.objects.get(id=user_id)
    user.send_activation_email(confirm_url)
