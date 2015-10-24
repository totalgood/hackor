# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pacs.model_utils


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0002_auto_20151024_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rawcommittees',
            name='candidate_maling_address',
        ),
        migrations.AddField(
            model_name='rawcommittees',
            name='candidate_mailing_address',
            field=pacs.model_utils.LongCharField(max_length=1000000000, null=True, db_column='maling_address', blank=True),
        ),
        migrations.AlterField(
            model_name='rawcommittees',
            name='committee_id',
            field=models.IntegerField(default=0, serialize=False, primary_key=True, blank=True),
        ),
    ]
