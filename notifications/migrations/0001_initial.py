# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-02 04:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('writers_block', '0001_initial'),
        ('portfolio', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('at_time', models.DateTimeField(auto_now_add=True)),
                ('not_type', models.CharField(choices=[('L', 'Liked'), ('C', 'Commented'), ('F', 'Followed'), ('S', 'Shared'), ('P', 'Piece Liked'), ('R', 'Piece Commented'), ('B', 'Piece Written')], max_length=1)),
                ('read', models.BooleanField(default=False)),
                ('block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='writers_block.Block')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_notifs', to=settings.AUTH_USER_MODEL)),
                ('piece', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portfolio.Piece')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-at_time'],
            },
        ),
    ]
