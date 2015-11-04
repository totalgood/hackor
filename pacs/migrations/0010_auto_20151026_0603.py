# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0009_auto_20151026_0537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workingtransactions',
            name='filer_id',
            field=models.ForeignKey(db_column='filer_id', blank=True, to='pacs.CampaignDetail', help_text='filer_id 17222 is not present in table working_committees', null=True),
        ),
    ]
