from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Action(models.Model):
    FOLLOWED = 'F'
    UNFOLLOWED = 'U'
    POSTED = 'P'
    LIKED = 'L'
    choices = (
        (FOLLOWED, 'Followed'),
        (UNFOLLOWED, 'Unfollowed'),
        (LIKED, 'Liked'),
        (POSTED, 'Added new entry on'),
    )

    _FOLLOWED_TEMPLATE = '<a href="{}" class="link">{}</a> has subscribed to <a href="{}" class="link">{}</a>'
    _UNFOLLOWED_TEMPLATE = '<a href="{}" class="link">{}</a> has unsubscribed from <a href="{}" class="link">{}</a>'
    _POSTED_TEMPLATE = '<a href="{}" class="link">{}</a> added a new<a href="{}" title={} class="link"> entry</a>'
    _LIKEED_TEMPLATE = '<a href="{}">{}</a>liked your<a href="{}">post</a>'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actions')
    action = models.CharField(max_length=1, choices=choices)
    created = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        verbose_name = "Action"
        verbose_name_plural = "Actions"
        ordering = ['-created']

    def __str__(self):
        if self.action == self.UNFOLLOWED:
            return self._UNFOLLOWED_TEMPLATE.format(
                self.user.get_absolute_url(),
                self.user.username,
                self.content_object.get_absolute_url(),
                self.content_object.username,
            )
        if self.action == self.FOLLOWED:
            return self._FOLLOWED_TEMPLATE.format(
                self.user.get_absolute_url(),
                self.user.username,
                self.content_object.get_absolute_url(),
                self.content_object.username,
            )
        if self.action == self.POSTED:
            return self._POSTED_TEMPLATE.format(
                    self.user.get_absolute_url(),
                    self.user.username,
                    self.content_object.get_absolute_url(),
                    self.content_object.title
            )


class Notification(models.Model):

    COMMENTED = 'C'
    FOLLOWED = 'F'
    UPVOTED  = 'U'
    DOWNVOTED = 'D'
    REPLIED = 'R'

    notification_types = (
        (COMMENTED, 'Commented'),
        (FOLLOWED, 'Followed'),
        (UPVOTED, 'Upvoted'),
        (DOWNVOTED, 'Downvoted'),
        (REPLIED, 'Replied'),
    )

    _COMMENTED_TEMPLATE = "<a href='{0}' class='link nohover' data-value='{3}'>{1}</a> commented on your <a href='{2}' class='link nohover'>Post </a>"
    _REPLIED_TEMPLATE = "<a href='{0}' class='link nohover' data-value='{2}'>{0}</a> has replied to your comment in <a href='{1}' class='link nohover'>Post</a>"

    from_user = models.ForeignKey(settings.AUTH_USER_MODEL)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications')
    post = models.ForeignKey('posts.Post', null=True, blank=True)
    comment = models.ForeignKey('posts.PostComment', null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(choices=notification_types, max_length=1)


    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created']

    def __str__(self):
        if self.notification_type == self.COMMENTED:
            return self._COMMENTED_TEMPLATE.format(self.from_user.get_absolute_url(), self.from_user.username, self.post.get_absolute_url(), self.id)
        if self.notification_type == self.REPLIED:
            return self._REPLIED_TEMPLATE.format(self.from_user.username, self.post.get_absolute_url(), self.id)
