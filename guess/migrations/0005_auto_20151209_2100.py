# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guess', '0004_drawing_actual'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drawing',
            name='actual',
            field=models.IntegerField(default=11),
        ),
    ]
