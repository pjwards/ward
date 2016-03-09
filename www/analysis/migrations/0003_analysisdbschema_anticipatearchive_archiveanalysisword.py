# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0005_auto_20151216_1646'),
        ('analysis', '0002_auto_20160218_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisDBSchema',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('avgpostlike', models.IntegerField(default=0)),
                ('avgpostcomment', models.IntegerField(default=0)),
                ('avgcomtlike', models.IntegerField(default=0)),
                ('avgcomtcomment', models.IntegerField(default=0)),
                ('lastupdatetime', models.DateTimeField()),
                ('group', models.ForeignKey(related_name='analysisSchema', to='archive.Group')),
            ],
        ),
        migrations.CreateModel(
            name='AnticipateArchive',
            fields=[
                ('id', models.CharField(primary_key=True, max_length=50, serialize=False)),
                ('message', models.TextField(null=True, blank=True)),
                ('time', models.DateTimeField()),
                ('status', models.CharField(max_length=10, default='temp')),
                ('group', models.ForeignKey(related_name='antiArchives', to='archive.Group')),
                ('user', models.ForeignKey(related_name='antiArchives', to='archive.FBUser')),
            ],
        ),
        migrations.CreateModel(
            name='ArchiveAnalysisWord',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('word', models.CharField(max_length=255)),
                ('count', models.IntegerField(default=1)),
                ('status', models.CharField(max_length=10, default='temp')),
                ('group', models.ForeignKey(related_name='archivewords', to='archive.Group')),
            ],
        ),
    ]
