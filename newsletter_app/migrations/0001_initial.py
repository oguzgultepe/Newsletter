# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_Pref',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_entry_date', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)])),
                ('reminder_mail_date', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)])),
                ('newsletter_mail_date', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)])),
                ('auto_send', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('priority', models.IntegerField()),
                ('requires_date', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title_german', models.CharField(max_length=50)),
                ('title_english', models.CharField(max_length=50)),
                ('text_german', models.CharField(max_length=1000)),
                ('text_english', models.CharField(max_length=1000)),
                ('link_german', models.URLField()),
                ('link_english', models.URLField()),
                ('publish_month', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('publish_year', models.IntegerField()),
                ('date', models.DateField()),
                ('finished', models.BooleanField(default=False)),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(to='newsletter_app.Category')),
            ],
        ),
    ]
