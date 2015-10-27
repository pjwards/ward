# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0008_auto_20151027_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='comment_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='group',
            name='post_count',
            field=models.IntegerField(default=0),
        ),
    ]
