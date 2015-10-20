# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0005_auto_20151015_1339'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.CharField(serialize=False, max_length=20, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('updated_time', models.DateTimeField()),
                ('privacy', models.CharField(max_length=30)),
                ('is_stored', models.BooleanField(default=False)),
            ],
        ),
    ]
