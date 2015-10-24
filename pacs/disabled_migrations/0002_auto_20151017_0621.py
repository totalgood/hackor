# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pacs.models

class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rawcommitteetransactions',
            options={},
        ),
        migrations.AlterField(
            model_name='rawcommitteetransactions',
            name='attest_by_name',
            field=pacs.models.LongCharField(max_length=1000000000),
        ),
        migrations.AlterField(
            model_name='rawcommitteetransactions',
            name='attest_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='rawcommitteetransactions',
            name='original_id',
            field=models.IntegerField(blank=True),
        ),
    ]
