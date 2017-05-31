# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-10 17:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20170410_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_visible',
            field=models.SmallIntegerField(choices=[(1, 'Yes'), (0, 'No')], default=0, verbose_name='Show email'),
        ),
    ]