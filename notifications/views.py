import json

from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Notification


class UserNotificationListView(ListView):
    model = Notification
    template_name = 'notifications.html'
    context_object_name = 'notes'
    paginate_by = 15
    paginate_orphans = 5

    def get_queryset(self):
        Notification.objects.filter(to_user=self.request.user).update(is_read=True)
        return Notification.objects.filter(to_user=self.request.user)


@login_required
def mark_as_read(request):
    if request.method == "POST" and request.is_ajax():
        data = request.POST.get('data')
        data = list(map(int, json.loads(data)))
        notes = Notification.objects.filter(id__in=data).update(is_read=True)

        return HttpResponse('hello')
