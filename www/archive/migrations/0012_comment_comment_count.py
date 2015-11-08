# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0011_user_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_count',
            field=models.IntegerField(default=0),
        ),
    ]
