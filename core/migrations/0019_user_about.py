# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-12 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20170411_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]