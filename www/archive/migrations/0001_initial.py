# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('url', models.CharField(max_length=255, blank=True, null=True)),
                ('title', models.CharField(max_length=255, blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('type', models.CharField(max_length=30, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Blacklist',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('count', models.IntegerField(default=0)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.CharField(serialize=False, max_length=20, primary_key=True)),
                ('created_time', models.DateTimeField()),
                ('message', models.TextField(blank=True, null=True)),
                ('like_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('is_show', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeletedComment',
            fields=[
                ('id', models.CharField(serialize=False, max_length=20, primary_key=True)),
                ('created_time', models.DateTimeField()),
                ('message', models.TextField(blank=True, null=True)),
                ('like_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('post', models.CharField(max_length=50)),
                ('parent', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeletedPost',
            fields=[
                ('id', models.CharField(serialize=False, max_length=50, primary_key=True)),
                ('created_time', models.DateTimeField()),
                ('updated_time', models.DateTimeField()),
                ('message', models.TextField(blank=True, null=True)),
                ('picture', models.CharField(max_length=255, blank=True, null=True)),
                ('comment_count', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('share_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.CharField(serialize=False, max_length=20, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('updated_time', models.DateTimeField()),
                ('privacy', models.CharField(max_length=30)),
                ('is_stored', models.BooleanField(default=False)),
                ('post_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('height', models.IntegerField(null=True)),
                ('width', models.IntegerField(null=True)),
                ('src', models.CharField(max_length=255, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.CharField(serialize=False, max_length=50, primary_key=True)),
                ('created_time', models.DateTimeField()),
                ('updated_time', models.DateTimeField()),
                ('message', models.TextField(blank=True, null=True)),
                ('picture', models.CharField(max_length=255, blank=True, null=True)),
                ('comment_count', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('share_count', models.IntegerField(default=0)),
                ('is_show', models.BooleanField(default=True)),
                ('group', models.ForeignKey(to='archive.Group', related_name='posts')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('status', models.CharField(default='new', max_length=30)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(null=True, to='archive.Comment', related_name='reports')),
                ('group', models.ForeignKey(to='archive.Group', related_name='reports')),
                ('post', models.ForeignKey(null=True, to='archive.Post', related_name='reports')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(serialize=False, max_length=20, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('picture', models.CharField(max_length=255, blank=True, null=True)),
                ('groups', models.ManyToManyField(to='archive.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(null=True, to='archive.Comment', related_name='wards')),
                ('group', models.ForeignKey(to='archive.Group', related_name='wards')),
                ('post', models.ForeignKey(null=True, to='archive.Post', related_name='wards')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='wards')),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='user',
            field=models.ForeignKey(to='archive.User', related_name='reports'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(to='archive.User', related_name='posts'),
        ),
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(null=True, to='archive.User', related_name='group_owner'),
        ),
        migrations.AddField(
            model_name='deletedpost',
            name='group',
            field=models.ForeignKey(to='archive.Group', related_name='delete_posts'),
        ),
        migrations.AddField(
            model_name='deletedpost',
            name='user',
            field=models.ForeignKey(to='archive.User', related_name='delete_posts'),
        ),
        migrations.AddField(
            model_name='deletedcomment',
            name='group',
            field=models.ForeignKey(to='archive.Group', related_name='delete_comments'),
        ),
        migrations.AddField(
            model_name='deletedcomment',
            name='user',
            field=models.ForeignKey(to='archive.User', related_name='delete_comments'),
        ),
        migrations.AddField(
            model_name='comment',
            name='group',
            field=models.ForeignKey(to='archive.Group', related_name='comments'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(null=True, to='archive.Comment', related_name='comments'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(to='archive.Post', related_name='comments'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to='archive.User', related_name='comments'),
        ),
        migrations.AddField(
            model_name='blacklist',
            name='group',
            field=models.ForeignKey(to='archive.Group', related_name='blacklist'),
        ),
        migrations.AddField(
            model_name='blacklist',
            name='user',
            field=models.ForeignKey(to='archive.User', related_name='blacklist'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='comment',
            field=models.ForeignKey(null=True, to='archive.Comment', related_name='attachments'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='media',
            field=models.ForeignKey(null=True, to='archive.Media', related_name='media'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='post',
            field=models.ForeignKey(null=True, to='archive.Post', related_name='attachments'),
        ),
    ]
