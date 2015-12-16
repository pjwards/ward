# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0004_useractivity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='user',
            field=models.ForeignKey(to='archive.FBUser', related_name='user_activities'),
        ),
    ]
