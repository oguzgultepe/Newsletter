# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter_app', '0003_remove_category_requires_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='created',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='submission',
            name='modified',
            field=models.DateTimeField(),
        ),
    ]
