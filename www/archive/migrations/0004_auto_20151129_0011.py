# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0003_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_show',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='post',
            name='is_show',
            field=models.BooleanField(default=True),
        ),
    ]
