# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0004_auto_20151129_0011'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('updated_time', models.DateTimeField(auto_created=True)),
                ('created_time', models.DateTimeField(auto_created=True)),
                ('comment', models.ForeignKey(null=True, to='archive.Comment', related_name='wards')),
                ('group', models.ForeignKey(related_name='wards', to='archive.Group')),
                ('post', models.ForeignKey(null=True, to='archive.Post', related_name='wards')),
                ('user', models.ForeignKey(related_name='wards', to='archive.User')),
            ],
        ),
    ]
