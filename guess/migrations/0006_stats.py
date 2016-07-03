# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guess', '0005_auto_20151209_2100'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('digit', models.IntegerField(default=11)),
                ('correctly_guessed', models.IntegerField(default=0)),
                ('incorrectly_guessed', models.IntegerField(default=0)),
            ],
        ),
    ]
