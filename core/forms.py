import logging

from slugify import slugify
from image_cropping import ImageCropWidget

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.utils.text import force_text

User = get_user_model()
logger = logging.getLogger(__name__)


class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        user.slug = slugify(user.username)
        if commit:
            user.is_active = False
            user.save()
        return user

    def is_valid(self):
        logger.info(force_text(self.errors))
        return super(UserCreationForm, self).is_valid()


class CustomUserChangeForm(UserChangeForm):

    birth_date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'country',
                  'location',
                  'homepage',
                  'birth_date',
                  'email_visible',
                  'avatar',
                  'avatar_cropping',
                  'about',
                  )
        # fields = '__all__'
        widgets = {
            'avatar': ImageCropWidget,
        }


    # def save(self, commit=False):
    #     print('blabla')
    #     return super(CustomUserChangeForm, self).save()

    def is_valid(self):
        logger.info(force_text(self.errors))
        return super(CustomUserChangeForm, self).is_valid()

