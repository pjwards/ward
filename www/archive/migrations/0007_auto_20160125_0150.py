# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0006_groupstorelist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupstorelist',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
