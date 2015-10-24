# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rawcandidatefilings',
            options={'managed': True, 'verbose_name': 'candidate filing'},
        ),
        migrations.AlterModelOptions(
            name='rawcommittees',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='rawcommitteetransactions',
            options={'verbose_name': 'raw transaction', 'verbose_name_plural': 'raw transactions'},
        ),
        migrations.AlterModelOptions(
            name='rawcommitteetransactionsammendedtransactions',
            options={'managed': True, 'verbose_name': 'working transaction', 'verbose_name_plural': 'working transactions'},
        ),
        migrations.AlterModelOptions(
            name='rawcommitteetransactionserrors',
            options={'managed': True, 'verbose_name': 'committee transaction error'},
        ),
        migrations.AlterModelOptions(
            name='workingcandidatecommittees',
            options={'managed': True, 'verbose_name': 'candidate committee'},
        ),
        migrations.AlterModelOptions(
            name='workingtransactions',
            options={'managed': False, 'verbose_name': 'working transaction', 'verbose_name_plural': 'working transactions'},
        ),
        migrations.AlterModelTable(
            name='workingtransactions',
            table='cc_working_transactions',
        ),
    ]
