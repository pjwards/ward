# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0011_monthcomment_monthpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthcomment',
            name='comment',
            field=models.ForeignKey(unique=True, to='archive.Comment'),
        ),
        migrations.AlterField(
            model_name='monthpost',
            name='post',
            field=models.ForeignKey(unique=True, to='archive.Post'),
        ),
    ]
