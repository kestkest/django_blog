from django.shortcuts import reverse, redirect
from django.conf.urls import url
from django.views.generic import DeleteView
from . import views
from .models import Post


urlpatterns = [
    url(r'^$', views.PostListView.as_view(), name='index'),
    url(r'addpost/$', views.add_post, name='PostCreate'),
    url(r'add-comment/(?P<slug>[-\w]+)/$', views.add_commment, name='add-comment'),
    url(r'editpost/(?P<slug>[-\w]+)/$', views.PostUpdateView.as_view(), name='PostUpdate'),
    url(r'deletepost/(?P<slug>[-\w]+)/$', views.PostDeleteView.as_view(), name='PostDelete'),
    url(r'^allposts/(?P<slug>[-\w]+)/$', views.UserPostListView.as_view(), name='user-posts'),
    url(r'^(?P<username>[-_.\w]+)/(?P<slug>[-\w]+)/$', views.PostDetailView.as_view(), name='PostDetail'),
    url(r'^(?P<slug>[-\w]+)/tag/(?P<name>[-\w]+)/$', views.ByTagUserPostListView.as_view(), name='post-by-tag'),
]

