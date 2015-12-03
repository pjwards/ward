# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='url',
            field=models.CharField(null=True, max_length=2083, blank=True),
        ),
        migrations.AlterField(
            model_name='deletedpost',
            name='picture',
            field=models.CharField(null=True, max_length=2083, blank=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='src',
            field=models.CharField(null=True, max_length=2083, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=models.CharField(null=True, max_length=2083, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.CharField(null=True, max_length=2083, blank=True),
        ),
    ]
