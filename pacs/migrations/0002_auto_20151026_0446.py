# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ccworkingtransactions',
            name='id',
            field=models.IntegerField(default=0, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='ccworkingtransactions',
            name='tran_id',
            field=models.IntegerField(help_text='Should be unique ID but isnt, e.g. 1171373 is duplicated.', null=True, blank=True),
        ),
    ]
