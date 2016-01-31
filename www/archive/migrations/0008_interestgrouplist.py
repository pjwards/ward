# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('archive', '0007_auto_20160125_0150'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterestGroupList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('group', models.ForeignKey(related_name='interest_group_list', to='archive.Group')),
                ('user', models.ForeignKey(related_name='interest_group_list', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
