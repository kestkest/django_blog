import os

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static


def get_avatar_path(user, filename):
    return os.path.join('img', 'users', str(user.id), 'avatar' + os.path.splitext(filename)[1])




