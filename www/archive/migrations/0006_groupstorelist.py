# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0005_auto_20151216_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupStoreList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('query', models.CharField(max_length=2083, null=True, blank=True)),
                ('status', models.CharField(default='new', max_length=30)),
                ('group', models.OneToOneField(to='archive.Group')),
            ],
        ),
    ]
