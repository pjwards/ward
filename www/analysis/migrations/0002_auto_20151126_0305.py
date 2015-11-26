# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0002_auto_20151124_2211'),
        ('analysis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpamContentList',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('text', models.TextField(null=True, blank=True)),
                ('status', models.CharField(max_length=10, default='temp')),
                ('group', models.ForeignKey(to='archive.Group')),
            ],
        ),
        migrations.CreateModel(
            name='SpamWordList',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('word', models.CharField(max_length=255)),
                ('count', models.IntegerField(default=1)),
                ('status', models.CharField(max_length=10, default='temp')),
                ('group', models.ForeignKey(to='archive.Group')),
            ],
        ),
        migrations.DeleteModel(
            name='SpamContent',
        ),
        migrations.DeleteModel(
            name='SpamList',
        ),
    ]
