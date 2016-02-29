# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0012_auto_20160227_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthcomment',
            name='comment',
            field=models.OneToOneField(to='archive.Comment'),
        ),
        migrations.AlterField(
            model_name='monthpost',
            name='post',
            field=models.OneToOneField(to='archive.Post'),
        ),
    ]
