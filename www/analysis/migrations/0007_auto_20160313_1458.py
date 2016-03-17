# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0017_group_oldest_date'),
        ('analysis', '0006_updatelist'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupDurations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('yeared', models.IntegerField(default=0)),
                ('monthed', models.IntegerField(default=0)),
                ('lastupdatetime', models.DateTimeField()),
                ('oldtimed', models.DateTimeField()),
                ('group', models.ForeignKey(to='archive.Group')),
            ],
        ),
        migrations.CreateModel(
            name='MonthlyWords',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('word', models.CharField(max_length=255)),
                ('weigh', models.IntegerField(default=0)),
                ('lastfeeddate', models.DateTimeField()),
                ('group', models.ForeignKey(to='archive.Group')),
            ],
        ),
        migrations.CreateModel(
            name='MonthTrendWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('datedtime', models.DateTimeField()),
                ('word', models.CharField(max_length=255)),
                ('weigh', models.IntegerField(default=1)),
                ('group', models.ForeignKey(to='archive.Group')),
            ],
        ),
        migrations.RemoveField(
            model_name='anticipatearchive',
            name='status',
        ),
    ]
