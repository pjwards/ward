# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('url', models.CharField(null=True, max_length=255, blank=True)),
                ('title', models.CharField(null=True, max_length=255, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('type', models.CharField(null=True, max_length=30, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Blacklist',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('count', models.IntegerField(default=0)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=20)),
                ('created_time', models.DateTimeField()),
                ('message', models.TextField(null=True, blank=True)),
                ('like_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DeletedComment',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=20)),
                ('created_time', models.DateTimeField()),
                ('message', models.TextField(null=True, blank=True)),
                ('like_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('post', models.CharField(max_length=50)),
                ('parent', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='DeletedPost',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=50)),
                ('created_time', models.DateTimeField()),
                ('updated_time', models.DateTimeField()),
                ('message', models.TextField(null=True, blank=True)),
                ('picture', models.CharField(null=True, max_length=255, blank=True)),
                ('comment_count', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('share_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('height', models.IntegerField(null=True)),
                ('width', models.IntegerField(null=True)),
                ('src', models.CharField(null=True, max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=50)),
                ('created_time', models.DateTimeField()),
                ('updated_time', models.DateTimeField()),
                ('message', models.TextField(null=True, blank=True)),
                ('picture', models.CharField(null=True, max_length=255, blank=True)),
                ('comment_count', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('share_count', models.IntegerField(default=0)),
                ('group', models.ForeignKey(to='archive.Group', related_name='posts')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('picture', models.CharField(null=True, max_length=255, blank=True)),
                ('groups', models.ManyToManyField(to='archive.Group')),
            ],
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
