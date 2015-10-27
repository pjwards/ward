# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0007_user_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='group',
            field=models.ForeignKey(to='archive.Group', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='group',
            field=models.ForeignKey(to='archive.Group', default=1),
            preserve_default=False,
        ),
    ]
