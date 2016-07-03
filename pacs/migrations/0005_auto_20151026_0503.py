# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0004_auto_20151026_0453'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workingcandidatecommittees',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='workingcandidatefilings',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='workingcommittees',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='workingtransactions',
            options={'managed': True},
        ),
    ]
