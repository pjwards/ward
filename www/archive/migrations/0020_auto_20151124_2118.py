# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0019_auto_20151124_2020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deletedcomment',
            name='comment_ptr',
        ),
        migrations.RemoveField(
            model_name='deletedpost',
            name='post_ptr',
        ),
        migrations.AddField(
            model_name='deletedcomment',
            name='comment_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='deletedcomment',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 12, 17, 28, 75195, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deletedcomment',
            name='group',
            field=models.ForeignKey(default=1, to='archive.Group', related_name='delete_comments'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deletedcomment',
            name='id',
            field=models.CharField(max_length=20, default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deletedcomment',
            name='like_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='deletedcomment',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='deletedcomment',
            name='parent',
            field=models.CharField(max_length=20, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deletedcomment',
            name='post',
            field=models.CharField(max_length=50, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deletedcomment',
            name='user',
            field=models.ForeignKey(default=1, to='archive.User', related_name='delete_comments'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deletedpost',
            name='comment_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='deletedpost',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 12, 18, 28, 237855, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deletedpost',
            name='group',
            field=models.ForeignKey(default=1, to='archive.Group', related_name='delete_posts'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deletedpost',
            name='id',
            field=models.CharField(max_length=50, default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deletedpost',
            name='like_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='deletedpost',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='deletedpost',
            name='picture',
            field=models.CharField(max_length=255, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='deletedpost',
            name='share_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='deletedpost',
            name='updated_time',
            field=models.DateTimeField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deletedpost',
            name='user',
            field=models.ForeignKey(default=1, to='archive.User', related_name='delete_posts'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='group',
            field=models.ForeignKey(to='archive.Group', related_name='comments'),
        ),
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(to='archive.Group', related_name='posts'),
        ),
    ]
