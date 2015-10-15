# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0004_auto_20151015_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='height',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='src',
            field=models.CharField(max_length=255, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='width',
            field=models.IntegerField(null=True),
        ),
    ]
