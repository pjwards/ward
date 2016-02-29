# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0013_auto_20160227_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthcomment',
            name='comment_count',
        ),
        migrations.RemoveField(
            model_name='monthcomment',
            name='like_count',
        ),
        migrations.RemoveField(
            model_name='monthpost',
            name='comment_count',
        ),
        migrations.RemoveField(
            model_name='monthpost',
            name='like_count',
        ),
        migrations.AddField(
            model_name='monthcomment',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='monthpost',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
