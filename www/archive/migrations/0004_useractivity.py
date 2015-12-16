# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('archive', '0003_auto_20151204_1753'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('post_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('group', models.ForeignKey(to='archive.Group', related_name='user_activities')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_activities')),
            ],
        ),
    ]
