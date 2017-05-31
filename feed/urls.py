from django.conf.urls import url

from .views import FeedListView

urlpatterns = [
    url(r'^$', FeedListView.as_view(), name='feed')
]