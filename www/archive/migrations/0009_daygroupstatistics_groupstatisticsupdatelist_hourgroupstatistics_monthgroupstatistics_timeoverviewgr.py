# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0008_interestgrouplist'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayGroupStatistics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('time', models.DateTimeField()),
                ('model', models.CharField(max_length=10)),
                ('count', models.IntegerField(default=0)),
                ('group', models.ForeignKey(to='archive.Group')),
            ],
        ),
        migrations.CreateModel(
            name='GroupStatisticsUpdateList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('method', models.CharField(max_length=30)),
                ('updated_time', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(to='archive.Group')),
            ],
        ),
        migrations.CreateModel(
            name='HourGroupStatistics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('time', models.DateTimeField()),
                ('model', models.CharField(max_length=10)),
                ('count', models.IntegerField(default=0)),
                ('group', models.ForeignKey(to='archive.Group')),
            ],
        ),
        migrations.CreateModel(
            name='MonthGroupStatistics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('time', models.DateTimeField()),
                ('model', models.CharField(max_length=10)),
                ('count', models.IntegerField(default=0)),
                ('group', models.ForeignKey(to='archive.Group')),
            ],
        ),
        migrations.CreateModel(
            name='TimeOverviewGroupStatistics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('time', models.IntegerField(default=0)),
                ('model', models.CharField(max_length=10)),
                ('count', models.IntegerField(default=0)),
                ('group', models.ForeignKey(to='archive.Group')),
            ],
        ),
        migrations.CreateModel(
            name='YearGroupStatistics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('time', models.DateTimeField()),
                ('model', models.CharField(max_length=10)),
                ('count', models.IntegerField(default=0)),
                ('group', models.ForeignKey(to='archive.Group')),
            ],
        ),
    ]
