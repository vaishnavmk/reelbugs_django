# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-21 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_auto_20170821_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='message_text',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]