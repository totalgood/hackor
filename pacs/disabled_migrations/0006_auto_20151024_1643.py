# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0005_auto_20151024_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importdates',
            name='file_hash',
            field=models.DecimalField(primary_key=True, db_column='id', default=0, serialize=False, decimal_places=1000, max_digits=1000, blank=True),
        ),
    ]
