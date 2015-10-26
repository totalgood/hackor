# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0006_auto_20151026_0504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workingcommittees',
            name='id',
        ),
        migrations.AlterField(
            model_name='workingcandidatefilings',
            name='id_nbr',
            field=models.IntegerField(help_text='0.32 unique', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='workingcommittees',
            name='committee_id',
            field=models.IntegerField(default=0, help_text='1.0 unique!', serialize=False, primary_key=True, blank=True),
        ),
    ]
