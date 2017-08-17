# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0002_auto_20170723_2054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='requires_date',
        ),
    ]
