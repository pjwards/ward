# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0009_daygroupstatistics_groupstatisticsupdatelist_hourgroupstatistics_monthgroupstatistics_timeoverviewgr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hourgroupstatistics',
            name='group',
        ),
        migrations.DeleteModel(
            name='HourGroupStatistics',
        ),
    ]
