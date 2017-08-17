# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0004_auto_20170723_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
