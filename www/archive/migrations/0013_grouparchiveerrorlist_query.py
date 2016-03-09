# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0012_grouparchiveerrorlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='grouparchiveerrorlist',
            name='query',
            field=models.CharField(max_length=2083, null=True, blank=True),
        ),
    ]
