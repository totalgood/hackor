# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guess', '0002_drawing_correct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drawing',
            name='correct',
            field=models.BooleanField(default=True),
        ),
    ]
