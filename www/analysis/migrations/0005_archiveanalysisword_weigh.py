# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0004_auto_20160229_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='archiveanalysisword',
            name='weigh',
            field=models.IntegerField(default=0),
        ),
    ]
