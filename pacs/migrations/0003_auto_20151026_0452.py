# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0002_auto_20151026_0446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ccworkingtransactions',
            name='id',
            field=models.IntegerField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
    ]
