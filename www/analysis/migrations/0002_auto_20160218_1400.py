# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0005_auto_20151216_1646'),
        ('analysis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpamList',
            fields=[
                ('id', models.CharField(serialize=False, max_length=50, primary_key=True)),
                ('message', models.TextField(null=True, blank=True)),
                ('time', models.DateTimeField()),
                ('status', models.CharField(max_length=10, default='temp')),
                ('group', models.ForeignKey(to='archive.Group', related_name='spamlist')),
                ('user', models.ForeignKey(to='archive.FBUser', related_name='spamlist')),
            ],
        ),
        migrations.RemoveField(
            model_name='spamcontentlist',
            name='group',
        ),
        migrations.AlterField(
            model_name='spamwordlist',
            name='group',
            field=models.ForeignKey(to='archive.Group', related_name='spamwords'),
        ),
        migrations.DeleteModel(
            name='SpamContentList',
        ),
    ]
