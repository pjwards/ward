# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0016_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='oldest_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
