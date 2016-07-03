# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guess', '0003_auto_20151203_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='drawing',
            name='actual',
            field=models.IntegerField(default=None),
        ),
    ]
