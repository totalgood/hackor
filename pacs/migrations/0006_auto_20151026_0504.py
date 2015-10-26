# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0005_auto_20151026_0503'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workingcandidatecommittees',
            name='id',
        ),
        migrations.AlterField(
            model_name='workingcandidatecommittees',
            name='committee_id',
            field=models.IntegerField(default=0, serialize=False, primary_key=True),
        ),
    ]
