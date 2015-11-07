# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0009_auto_20151027_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='comment',
            field=models.ForeignKey(to='archive.Comment', null=True, related_name='attachments'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='media',
            field=models.ForeignKey(to='archive.Media', null=True, related_name='media'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='post',
            field=models.ForeignKey(to='archive.Post', null=True, related_name='attachments'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(to='archive.Comment', null=True, related_name='comments'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(to='archive.Post', related_name='comments'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to='archive.User', related_name='comments'),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(to='archive.User', related_name='posts'),
        ),
    ]
