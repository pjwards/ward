# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0018_remove_group_oldest_date'),
        ('analysis', '0007_auto_20160313_1458'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklyWords',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('word', models.CharField(max_length=255)),
                ('weigh', models.IntegerField(default=0)),
                ('lastfeeddate', models.DateTimeField()),
                ('group', models.ForeignKey(to='archive.Group')),
            ],
        ),
        migrations.CreateModel(
            name='WordsDiction',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('word', models.CharField(max_length=255)),
                ('count', models.IntegerField(default=0)),
                ('group', models.ForeignKey(to='archive.Group')),
            ],
        ),
        migrations.RemoveField(
            model_name='groupdurations',
            name='group',
        ),
        migrations.AddField(
            model_name='anticipatearchive',
            name='status',
            field=models.CharField(default='temp', max_length=10),
        ),
        migrations.AddField(
            model_name='monthtrendword',
            name='lastfeeddate',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 17, 9, 31, 55, 152313, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='GroupDurations',
        ),
    ]
