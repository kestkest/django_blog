from django.shortcuts import render
from django.views.generic import ListView

from posts.models import Post


class FeedListView(ListView):
    context_object_name = 'posts'
    paginate_by = 10
    paginate_orphans = 3
    template_name = 'feed.html'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            followees = self.request.user.followees.all()
            return Post.objects.filter(author__in=followees)
        return []
# Create your views here.
