# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0012_comment_comment_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(related_name='group_owner', to='archive.User', default=10205748261478529),
            preserve_default=False,
        ),
    ]
