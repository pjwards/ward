# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0005_archiveanalysisword_weigh'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpdateList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('method', models.CharField(max_length=30)),
                ('updated_time', models.DateTimeField(auto_now_add=True)),
                ('data', models.TextField(null=True, blank=True)),
            ],
        ),
    ]
