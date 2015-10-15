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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('url', models.CharField(max_length=255, blank=True)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('description', models.TextField(blank=True)),
                ('type', models.CharField(max_length=30, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField()),
                ('message', models.TextField(blank=True)),
                ('like_count', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(blank=True, to='archive.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('height', models.IntegerField()),
                ('width', models.IntegerField()),
                ('src', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField()),
                ('updated_time', models.DateTimeField()),
                ('message', models.TextField(blank=True)),
                ('picture', models.CharField(max_length=255, blank=True)),
                ('like_count', models.IntegerField(default=0)),
                ('shares', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(to='archive.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to='archive.User'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='comment',
            field=models.ForeignKey(blank=True, to='archive.Comment'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='media',
            field=models.ForeignKey(blank=True, to='archive.Media'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='post',
            field=models.ForeignKey(blank=True, to='archive.Post'),
        ),
    ]
