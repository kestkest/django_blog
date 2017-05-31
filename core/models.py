import os
import uuid
import datetime

from slugify import slugify
from image_cropping import ImageRatioField

from django.db import models
from django.core.validators import EmailValidator, ValidationError
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone, six
from django.shortcuts import reverse
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from notifications.models import Action
from .helpers import get_avatar_path


email_options = (
    (1, 'Yes'),
    (0, 'No'),
)


class MyUserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, username, password, **kwargs):
        if not email:
            raise ValidationError('Email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username, **kwargs)
        user.slug = slugify(user.username)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, username, password, **kwargs):
        kwargs.setdefault('is_superuser', False)
        kwargs.setdefault('is_staff', False)
        return self._create_user(email, username, password, **kwargs)

    def create_superuser(self, email, username, password, **kwargs):
        # kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, username, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
            verbose_name='Email address',
            unique=True,
            error_messages={
                'email': 'A user with that email already exists.',
            }
    )

    activation_key = models.CharField(max_length=50, blank=True)
    key_expires = models.DateTimeField(default=timezone.now, blank=True)

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        error_messages={
            'unique': "A user with that username already exists.",
        },
        null=True
    )
    slug = models.SlugField(blank=True, null=True, max_length=150)
    first_name = models.CharField(verbose_name='First name', max_length=100, blank=True)
    last_name = models.CharField(max_length=120, blank=True)
    avatar = models.ImageField(upload_to=get_avatar_path,
                               blank=True,
                               null=True,
                               verbose_name='avatar')
    avatar_cropping = ImageRatioField('avatar', size='300x300', size_warning=True)
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    is_active = models.BooleanField(
            verbose_name='active',
            default=False,
            help_text='Designates whether this user should be treated as '
                      'active. Unselect this instead of deleting accounts.'
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )

    country = models.CharField(max_length=50, blank=True)
    location = models.CharField(verbose_name='City/State', max_length=50, blank=True)
    homepage = models.CharField(max_length=255,  blank=True)
    email_visible = models.SmallIntegerField(verbose_name='Show email', choices=email_options, default=0)
    birth_date = models.DateField(null=True, blank=True, verbose_name='Date of birth')
    about = models.TextField(max_length=500, blank=True)
    followees = models.ManyToManyField('self',
                                       related_name='follower',
                                       blank=True,
                                       verbose_name='Followees',
                                       symmetrical=False,
                                       )
    post_action = GenericRelation(Action)
    # followers = models.ManyToManyField('self', blank=True, related_name='followee', verbose_name='Followers')

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    @staticmethod
    def generate_key():
        return uuid.uuid4().hex

    def is_following(self, other):
        _LINK = '<a href="#" class="follow {0}" data-slug="{1}" data-action="{2}">{3}</a>'
        isfollow = self.followees.filter(slug=other).exists()
        class_attr = 'remove' if isfollow else 'add'
        innertext = 'Unfollow' if isfollow else 'Follow'
        link = _LINK.format(class_attr, other, reverse('core:follow'), innertext)
        return link

    def follow(self, other):
        self.followees.add(other)

    def unfollow(self, other):
        self.followees.remove(other)

    def delete_unused_avatar(self):
        avatar_subdir = '/'.join(self.avatar.url.split('/')[2:-1])
        avatar_abs_dir = os.path.join(settings.MEDIA_ROOT, avatar_subdir)
        cur_avatar = self.avatar.name.split('/')[-1]
        for root, dirs, files in os.walk(avatar_abs_dir):
            for file in files:
                if file != cur_avatar:
                    os.remove(os.path.join(root, file))

    def reset_token(self):
        self.activation_key = User.generate_key()
        self.key_expires = timezone.now()
        self.save()

    def validate_token(self):
        return self.key_expires + datetime.timedelta(days=3) > timezone.now()

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def email_user(self, subj, message, _from=None, **kwargs):
        send_mail(subj, message, _from, [self.email], **kwargs)

    def get_absolute_url(self):
        if not self.slug:
            self.slug = slugify(self.username)
        return reverse('core:UserDetail', args=[str(self.slug)])

    def get_avatar(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return static('/img/users/user_noimage.png')

    def send_activation_email(self, url):
        _CONFIRM = 'Hello {}, please confirm your email to complete registration!'
        subj = _CONFIRM.format(self.username)
        msg = 'press this link to be able to post'
        from_email = settings.EMAIL_HOST_USER
        to_email = self.email
        confirm_url = url
        html_content = render_to_string('email_confirmation.html', {'username': self.username, 'url': confirm_url})
        send_mail(
                subject=subj,
                from_email=from_email,
                recipient_list=[to_email],
                message=msg,
                html_message=html_content
        )
        print('done')

    def __str__(self):
        return '%s' % (self.username,)


