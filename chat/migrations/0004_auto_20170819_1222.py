# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-19 06:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0003_auto_20170819_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='users',
        ),
        migrations.AddField(
            model_name='room',
            name='users',
            field=models.ManyToManyField(related_name='rooms', to=settings.AUTH_USER_MODEL),
        ),
    ]