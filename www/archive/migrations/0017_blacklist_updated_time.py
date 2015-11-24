# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0016_comment_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='blacklist',
            name='updated_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 9, 18, 18, 687905, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
