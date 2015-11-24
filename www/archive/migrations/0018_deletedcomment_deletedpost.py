# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0017_blacklist_updated_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeletedComment',
            fields=[
                ('comment_ptr', models.OneToOneField(auto_created=True, parent_link=True, serialize=False, primary_key=True, to='archive.Comment')),
            ],
            bases=('archive.comment',),
        ),
        migrations.CreateModel(
            name='DeletedPost',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, parent_link=True, serialize=False, primary_key=True, to='archive.Post')),
            ],
            bases=('archive.post',),
        ),
    ]
