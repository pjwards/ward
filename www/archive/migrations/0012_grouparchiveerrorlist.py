# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0011_fbuser_updated_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupArchiveErrorList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('error_count', models.IntegerField(default=1)),
                ('message', models.TextField(blank=True, null=True)),
                ('group', models.OneToOneField(to='archive.Group')),
            ],
        ),
    ]
