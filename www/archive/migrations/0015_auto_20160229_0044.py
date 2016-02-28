# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0014_auto_20160228_1235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthcomment',
            name='score',
        ),
        migrations.RemoveField(
            model_name='monthpost',
            name='score',
        ),
    ]
