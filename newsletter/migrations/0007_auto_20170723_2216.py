# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0006_auto_20170723_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='publish_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 22, 20, 16, 40, 78046, tzinfo=utc)),
        ),
    ]
