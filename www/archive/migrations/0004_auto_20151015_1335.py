# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0003_comment_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='comment',
            field=models.ForeignKey(null=True, to='archive.Comment'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='media',
            field=models.ForeignKey(null=True, to='archive.Media'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='post',
            field=models.ForeignKey(null=True, to='archive.Post'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='type',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(null=True, to='archive.Comment'),
        ),
        migrations.AlterField(
            model_name='post',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
