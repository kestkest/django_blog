# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 17:40
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20170318_0713'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='depth',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='postcomment',
            name='path',
            field=posts.models.ListField(blank=True, verbose_name="comment's parents path"),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='content',
            field=ckeditor.fields.RichTextField(help_text='Write something..', max_length=1000, verbose_name='Commentary body'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
