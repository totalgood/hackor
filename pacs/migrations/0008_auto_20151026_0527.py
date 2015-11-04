# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0007_auto_20151026_0510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workingtransactions',
            name='id',
        ),
        migrations.AlterField(
            model_name='workingtransactions',
            name='tran_id',
            field=models.IntegerField(default=0, help_text='1.0 fraction unique', serialize=False, verbose_name='transaction ID', primary_key=True),
        ),
    ]
