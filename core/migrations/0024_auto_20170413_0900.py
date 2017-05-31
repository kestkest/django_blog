# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-13 09:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20170413_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followees',
            field=models.ManyToManyField(blank=True, related_name='_user_followees_+', to=settings.AUTH_USER_MODEL, verbose_name='Followees'),
        ),
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='_user_followers_+', to=settings.AUTH_USER_MODEL, verbose_name='Followers'),
        ),
    ]
