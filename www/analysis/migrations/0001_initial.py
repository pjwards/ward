# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpamContentList',
            fields=[
                ('id', models.CharField(serialize=False, max_length=50, primary_key=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('status', models.CharField(default='temp', max_length=10)),
                ('group', models.ForeignKey(to='archive.Group')),
            ],
        ),
        migrations.CreateModel(
            name='SpamWordList',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('word', models.CharField(max_length=255)),
                ('count', models.IntegerField(default=1)),
                ('status', models.CharField(default='temp', max_length=10)),
                ('group', models.ForeignKey(to='archive.Group')),
            ],
        ),
    ]
