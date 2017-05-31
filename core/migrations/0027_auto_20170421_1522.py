# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-21 15:22
from __future__ import unicode_literals

import core.helpers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20170413_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=core.helpers.get_avatar_path, verbose_name='avatar'),
        ),
    ]