# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0018_deletedcomment_deletedpost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='post',
            name='is_deleted',
        ),
    ]
