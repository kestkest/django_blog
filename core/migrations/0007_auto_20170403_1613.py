# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-03 16:13
from __future__ import unicode_literals

import core.helpers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_user_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=core.helpers.get_avatar_path),
        ),
    ]
