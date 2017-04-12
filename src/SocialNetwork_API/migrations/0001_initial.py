# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-12 03:56
from __future__ import unicode_literals

import SocialNetwork_API.models.user
import SocialNetwork_API.models.user_types
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
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
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(default='', error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=20, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username')),
                ('email', models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, help_text='245 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_disabled', models.BooleanField(default=False)),
                ('manager_id', models.PositiveIntegerField(default=0)),
                ('Phone', models.CharField(default='', max_length=255)),
                ('MemoryUsed', models.FloatField(default=0)),
                ('TotalMemory', models.FloatField(default=10)),
                ('user_type', SocialNetwork_API.models.user_types.TinyIntegerField(default=1)),
                ('Sex', models.IntegerField(default=3)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'db_table': 'auth_user',
                'swappable': 'AUTH_USER_MODEL',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', SocialNetwork_API.models.user.UserManager()),
            ],
        ),
    ]