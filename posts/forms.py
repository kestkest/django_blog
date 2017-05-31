from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Post, Tag, PostComment


class PostForm(forms.ModelForm):

    title = forms.CharField(max_length=200, widget=forms.TextInput())
    # body = forms.CharField(widget=CKEditorWidget())
    tags = forms.CharField(widget=forms.TextInput(), help_text='use spaces to separate tag like this "python django"',
                           required=False)

    class Meta:
        model = Post
        fields = ('title', 'body', 'tags')


class PostCommentForm(forms.ModelForm):
    parent = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'parent', 'value': 0}), required=False, label='')
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4,
                                                           'style': 'resize:none',
                                                           'placeholder': 'Join the discussion...'
                                                           }))

    class Meta:
        model = PostComment
        fields = ('content',)






