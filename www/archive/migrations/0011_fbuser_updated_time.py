# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0010_auto_20160217_0113'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbuser',
            name='updated_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 27, 9, 45, 25, 51780, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
