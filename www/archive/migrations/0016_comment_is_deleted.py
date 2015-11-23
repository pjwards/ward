# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0015_auto_20151123_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_deleted',
            field=models.BigIntegerField(default=False),
        ),
    ]
