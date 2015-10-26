# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0001_initial'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='ccworkingtransactions',
        #     name='id',
        # ),
        migrations.AlterField(
            model_name='ccworkingtransactions',
            name='tran_id',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
    ]
