# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0002_auto_20151124_2211'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('status', models.CharField(max_length=30, default='new')),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(to='archive.Comment', null=True, related_name='reports')),
                ('group', models.ForeignKey(to='archive.Group', related_name='reports')),
                ('post', models.ForeignKey(to='archive.Post', null=True, related_name='reports')),
                ('user', models.ForeignKey(to='archive.User', related_name='reports')),
            ],
        ),
    ]
