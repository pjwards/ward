# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0014_auto_20151121_2351'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blacklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('group', models.ForeignKey(to='archive.Group', related_name='blacklist')),
                ('user', models.ForeignKey(to='archive.User', related_name='blacklist')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='is_deleted',
            field=models.BigIntegerField(default=False),
        ),
    ]
