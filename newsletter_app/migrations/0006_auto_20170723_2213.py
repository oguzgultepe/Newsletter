# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter_app', '0005_auto_20170723_2152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='publish_month',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='publish_year',
        ),
        migrations.AddField(
            model_name='submission',
            name='publish_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
