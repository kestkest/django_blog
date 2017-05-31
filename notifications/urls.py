from django.conf.urls import url

from .views import UserNotificationListView, mark_as_read

urlpatterns = [
    url(r'(?P<username>[-_.\w]+)/$', UserNotificationListView.as_view(), name='notification-list'),
    url(r'^mark_as_read$', mark_as_read, name='mark-as-read'),
]