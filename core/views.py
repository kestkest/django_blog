import datetime
import uuid
import os

from collections import OrderedDict

from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView, UpdateView
from django.contrib.auth import get_user_model, authenticate, login, mixins, decorators
from django.template.defaultfilters import date
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from notifications.models import Action, Notification
from .forms import CustomUserCreationForm, CustomUserChangeForm
from posts.forms import PostCommentForm, Post
from .tasks import send_activation_mail

User = get_user_model()

CONFIRM = 'Hello {}, please confirm your email to complete registration!'


def followees(request):

    return render(request, 'followees.html')


def confirmation(request, username, token):
    user = User.objects.filter(activation_key=token)[0]
    if user.validate_token():
        user.is_active = True
        user.save()
        return render(request, 'core/verification_success.html')
    reset_url = reverse('core:reset-token', args=(token, ))
    return render(request, 'core/verification_fail.html', {'url': reset_url})


def reset_token(request, token):
    user = User.objects.filter(activation_key=token)[0]
    user.reset_token()
    subj = CONFIRM.format(user.username)
    msg = 'press this link to be able to post'
    from_email = settings.EMAIL_HOST_USER
    to_email = user.email
    confirm_url = request.build_absolute_uri(reverse('core:confirmation',
                                                     args=(user.username, user.activation_key)))
    html_content = render_to_string('email_confirmation.html', {'username': user.username, 'url': confirm_url})
    send_mail(
            subject=subj,
            from_email=from_email,
            recipient_list=[to_email],
            message=msg,
            html_message=html_content
    )
    return render(request, 'core/email_verification_sent.html')


def signup(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.activation_key = User.generate_key()

            confirm_url = request.build_absolute_uri(reverse('core:confirmation',
                                                             args=(user.username, user.activation_key)))
            user.save()
            send_activation_mail.delay(user.id, confirm_url)
            return render(request, 'core/email_verification_sent.html')
    return render(request, 'core/signup.html', {'form': form})


class UserDetailView(DetailView):
    model = User
    context_object_name = 'user_obj'
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data()
        context.update({'data': self.get_info()})
        return context

    def get_info(self):
        data = {}
        user = self.object
        data.update(dict(country=user.country,
                         registred=date(user.date_joined),
                         fullname=user.get_full_name()),
                         posts=len(user.posts.all()),
                         homepage=user.homepage
                    )
        data['email'] = ""
        if user.email_visible:
            data['email'] = user.email
        data['last login'] = user.last_login
        if user.birth_date:
            data['birthday'] = user.birth_date
        else:
            data['birthday'] = ""
        data = OrderedDict(sorted(data.items(), key=lambda x: x[0]))
        return data


class UserUpdateView(mixins.UserPassesTestMixin, UpdateView):
    form_class = CustomUserChangeForm
    model = User
    template_name = 'core/user_update.html'
    context_object_name = 'user_obj'

    def form_valid(self, form):
        if self.request.FILES:
            self.object.delete_unused_avatar()
        return super(UserUpdateView, self).form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object()


@decorators.login_required()
def follow(request):
    if request.method == 'POST' and request.is_ajax():
        slug = request.POST.get('slug')
        other = User.objects.get(slug=slug)
        if request.POST.get('action') == 'add':
            request.user.follow(other)
            action = Action.objects.create(
                    user=request.user,
                    content_object=other,
                    action=Action.FOLLOWED
            )
        if request.POST.get('action') == 'remove':
            request.user.unfollow(other)
            action = Action.objects.create(
                    user=request.user,
                    content_object=other,
                    action=Action.UNFOLLOWED
            )
        print(request.user.followees.all())
        return HttpResponse(content='PRIVET PUNYA')


def like(request):
    pass