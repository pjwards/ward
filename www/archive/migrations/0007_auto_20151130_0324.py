# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0006_auto_20151130_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ward',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ward',
            name='updated_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
