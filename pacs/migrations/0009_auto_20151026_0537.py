# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0008_auto_20151026_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workingtransactions',
            name='filer_id',
            field=models.ForeignKey(blank=True, to='pacs.CampaignDetail', help_text='filer_id 17222 is not present in table working_committees', null=True),
        ),
    ]
