# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-21 03:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SocialNetwork_API', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='memoryUsed',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='totalMemory',
            field=models.FloatField(default=10),
        ),
    ]