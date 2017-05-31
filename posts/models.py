from markdown import markdown
from slugify import slugify
from django.db import models
from django.conf import settings
from datetime import datetime
from django.shortcuts import reverse
from django.db.models import Count
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from ckeditor.fields import RichTextField

from notifications.models import Action, Notification


class ListField(models.Field):

    description = "List field. Items are separated with semicolons(e.g. '123;23;35')."

    def __init__(self, *args, **kwargs):
        self.separator = ';'
        super(ListField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(ListField, self).deconstruct()
        if self.separator != ';':
            kwargs['separator'] = self.separator
        return name, path, args, kwargs

    def to_python(self, value):
        if not value or value == 'None':
            return []

        value = [int(val) for val in value.split(self.separator)]
        return value

    def get_prep_value(self, value):
        value = ';'.join(map(str, value))
        return value

    # def get_db_prep_value(self, value, connection, prepared=False):
    #     value = ';'.join(map(str, value))
    #     return value

    def get_internal_type(self):
        return 'TextField'

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return self.to_python(value)


class Post(models.Model):
    title = models.CharField(verbose_name="Заголовок", blank=False, max_length=200)
    slug = models.SlugField(max_length=200, null=True, blank=True, allow_unicode=True)
    # body = models.TextField(verbose_name="Post text", blank=False)
    body = RichTextField(verbose_name="Post text", blank=False)
    created = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Date changed", auto_now=True)
    rating = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts")
    views = models.IntegerField(default=0, verbose_name='views')
    likes = GenericRelation(Action)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created']

    def __str__(self):
        return '{}: Title:{}, Author:{}'.format('Post', self.title, self.author)

    def add_view(self):
        self.views += 1
        self.save()
        return self.views

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        else:
            self.updated = datetime.now()
        slug = slugify('{}-{}'.format(self.pk, self.title.lower()))
        if self.slug != slug:
            self.slug = slugify('{}-{}'.format(self.pk, self.title.lower()))

        super().save(*args, **kwargs)

    def get_preface(self):
        if len(self.body) > 255:
            return '{}...'.format(self.body[:255])
        else:
            return self.body

    def create_tags(self, tags):
        tags = tags.strip().split()
        for tag in tags:
            Tag.objects.get_or_create(name=tag.lower(), post=self)

    def get_preface(self, text):
        import re
        text = text[:223]
        text += '...'
        stack = []
        pattern = r'<(/*\w+)>'
        res = re.findall(pattern, text)
        for i in res:
            if not i.startswith('/'):
                stack.append(i)
            else:
                if stack:
                    if i[1:] == stack[-1]:
                        stack.pop()

        while stack:
            text += '</{}>'.format(stack.pop())
        return text

    def get_comments(self):
        pass

    def get_absolute_url(self):
        return reverse('posts:PostDetail', kwargs={'username': self.author.username, 'slug': self.slug})

    def get_preface_as_markdown(self):
        return markdown(self.get_preface(), safe_mode='escape')


class Tag(models.Model):
    name = models.CharField(max_length=50)
    post = models.ForeignKey(Post, related_name='tags')

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        unique_together = (('name', 'post'),)
        index_together = (['name', 'post'],)

    def __str__(self):
        return self.name

    @staticmethod
    def get_popular():
        tags = Tag.objects.all()
        result = {}
        for tag in tags:
            if tag.name in result:
                result[tag.name] += 1
            else:
                result[tag.name] = 1
        result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        return result[:20]

    @staticmethod
    def popular():
        query = Tag.objects.values('name').annotate(count=Count('name')).order_by('-count')[:20]
        return query

    def get_by_user(self):
        return reverse('posts:post-by-tag', kwargs={'slug': self.post.author.slug, 'name': self.name})


class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    # content = RichTextField("Add your commentary", max_length=1000, blank=False)
    content = models.TextField("Add a comment:", max_length=1000, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments')
    path = ListField(verbose_name="list of ids stored in the path attribute of parent comment if exists", blank=True, default=[], editable=False)
    depth = models.PositiveSmallIntegerField(default=0)
    rating = models.IntegerField(default=0)


    class Meta:
        verbose_name = 'Post comment'
        verbose_name_plural = "Post comments"
        ordering = ['path']

    def __str__(self):
        return '{0}@{1}'.format(self.author.username, self.created)

    def path_as_string(self):
        return ''.join(map(str, self.path))








