from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^update/(?P<slug>[-\w]+)/$', views.UserUpdateView.as_view(), name='user-update'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^(?P<slug>[-\w]+)/$', views.UserDetailView.as_view(), name='UserDetail'),
    url(r'^subs', views.followees, name='followees'),
    url(r'^confirm/reset/(?P<token>[\w\d]+)/$', views.reset_token, name='reset-token'),
    url(r'^confirm/(?P<username>[-_.\w]+)/(?P<token>[\w\d]+)', views.confirmation, name='confirmation'),
    url(r'^follow$', views.follow, name='follow'),
]
