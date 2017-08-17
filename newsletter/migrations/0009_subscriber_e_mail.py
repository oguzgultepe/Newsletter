# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0008_auto_20170803_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='e_mail',
            field=models.EmailField(default='some@somemail.com', max_length=254),
            preserve_default=False,
        ),
    ]
