# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0002_auto_20151203_2358'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='FBUser',
        ),
    ]
