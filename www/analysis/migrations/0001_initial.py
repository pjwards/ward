# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SpamContent',
            fields=[
                ('id', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('text', models.TextField(null=True, blank=True)),
                ('status', models.CharField(max_length=10, default='temp')),
            ],
        ),
        migrations.CreateModel(
            name='SpamList',
            fields=[
                ('word', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('count', models.IntegerField(default=1)),
                ('status', models.CharField(max_length=10, default='temp')),
            ],
        ),
    ]
