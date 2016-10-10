# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drawing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('values_array', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(default=0.0), size=None)),
                ('guess', models.IntegerField(default=None)),
                ('confidence', models.FloatField(default=None)),
                ('tiny_array', django.contrib.postgres.fields.ArrayField(default=[], base_field=models.FloatField(default=0.0), size=None)),
                ('correct', models.BooleanField(default=True)),
                ('actual', models.IntegerField(default=11)),
            ],
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('digit', models.IntegerField(default=11)),
                ('correctly_guessed', models.IntegerField(default=0)),
                ('incorrectly_guessed', models.IntegerField(default=0)),
            ],
        ),
    ]
