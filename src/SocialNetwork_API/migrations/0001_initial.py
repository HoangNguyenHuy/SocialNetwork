# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-12 02:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachments',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('post_id', models.PositiveIntegerField(default=0)),
                ('data_id', models.PositiveIntegerField(default=0)),
            ],
            options={
                'db_table': 'sn_attachments',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('post_id', models.PositiveIntegerField(default=0)),
                ('user_id', models.PositiveIntegerField(default=0)),
                ('reply_to_comment_id', models.PositiveIntegerField(default=0)),
                ('comment', models.TextField(default='')),
            ],
            options={
                'db_table': 'sn_comments',
            },
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(default='', max_length=255)),
                ('data_status', models.CharField(default='', max_length=255)),
                ('capacity', models.FloatField(default=0)),
                ('approval', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'sn_datas',
            },
        ),
        migrations.CreateModel(
            name='Download',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data_id', models.PositiveIntegerField(default=0)),
                ('user_id', models.PositiveIntegerField(default=0)),
            ],
            options={
                'db_table': 'sn_downloads',
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.PositiveIntegerField(default=0)),
                ('friend_user_id', models.PositiveIntegerField(default=0)),
            ],
            options={
                'db_table': 'sn_friends',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.PositiveIntegerField(default=0)),
                ('group_name', models.CharField(default='', max_length=255)),
                ('number_of_members', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'sn_groups',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.PositiveIntegerField(default=0)),
                ('group_id', models.PositiveIntegerField(default=0)),
            ],
            options={
                'db_table': 'sn_members',
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.PositiveIntegerField(default=0)),
                ('content', models.TextField()),
                ('status', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'sn_posts',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.PositiveIntegerField(default=0)),
                ('post_id', models.PositiveIntegerField(default=0)),
            ],
            options={
                'db_table': 'sn_tags',
            },
        ),
    ]
