# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0003_analysisdbschema_anticipatearchive_archiveanalysisword'),
    ]

    operations = [
        migrations.AddField(
            model_name='archiveanalysisword',
            name='commentnum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='archiveanalysisword',
            name='likenum',
            field=models.IntegerField(default=0),
        ),
    ]
