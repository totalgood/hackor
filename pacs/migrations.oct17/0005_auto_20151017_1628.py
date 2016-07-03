# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0004_clean_committee_transactions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidatebystate',
            options={'managed': False, 'verbose_name_plural': 'candidates by state'},
        ),
        migrations.AlterModelOptions(
            name='candidatesumbydate',
            options={'managed': False, 'verbose_name_plural': 'candidate sums by date'},
        ),
        migrations.AlterModelOptions(
            name='ccgrassrootsinstate',
            options={'managed': False, 'verbose_name': 'grass roots in-state total', 'verbose_name_plural': 'grass roots in-state totals'},
        ),
        migrations.AlterModelOptions(
            name='ccworkingtransactions',
            options={'managed': False, 'verbose_name': 'working transaction', 'verbose_name_plural': 'working transactions'},
        ),
        migrations.AlterModelOptions(
            name='committeetransactions',
            options={'managed': True, 'verbose_name': 'transaction', 'verbose_name_plural': 'transactions'},
        ),
        migrations.AlterModelOptions(
            name='directioncodes',
            options={'managed': False, 'verbose_name': 'direction', 'verbose_name_plural': 'directions'},
        ),
        migrations.AlterModelOptions(
            name='documentation',
            options={'managed': False, 'verbose_name': 'document', 'verbose_name_plural': 'documents'},
        ),
        migrations.AlterModelOptions(
            name='hackoregondbstatus',
            options={'managed': False, 'verbose_name': 'database status', 'verbose_name_plural': 'database status'},
        ),
        migrations.AlterModelOptions(
            name='importdates',
            options={'managed': False, 'verbose_name': 'file import date', 'verbose_name_plural': 'file import dates'},
        ),
        migrations.AlterModelOptions(
            name='oregonbycontributions',
            options={'managed': False, 'verbose_name': 'contribution type', 'verbose_name_plural': 'contribution types'},
        ),
        migrations.AlterModelOptions(
            name='oregonbypurposecodes',
            options={'managed': False, 'verbose_name': 'purpose', 'verbose_name_plural': 'purposes'},
        ),
        migrations.AlterModelOptions(
            name='oregoncommitteeagg',
            options={'managed': False, 'verbose_name': 'pac aggregate', 'verbose_name_plural': 'pac aggregates'},
        ),
        migrations.AlterModelOptions(
            name='rawcandidatefilings',
            options={'managed': False, 'verbose_name': 'candidate filing', 'verbose_name_plural': 'candidate filings'},
        ),
        migrations.AlterModelOptions(
            name='rawcommittees',
            options={'managed': False, 'verbose_name': 'committee', 'verbose_name_plural': 'committees'},
        ),
        migrations.AlterModelOptions(
            name='rawcommitteetransactions',
            options={'verbose_name': 'raw transaction', 'verbose_name_plural': 'raw transactions'},
        ),
        migrations.AlterModelOptions(
            name='rawcommitteetransactionsammendedtransactions',
            options={'managed': False, 'verbose_name': 'ammended transaction', 'verbose_name_plural': 'ammended transactions'},
        ),
        migrations.AlterModelOptions(
            name='rawcommitteetransactionserrors',
            options={'managed': False, 'verbose_name': 'transaction error', 'verbose_name_plural': 'transaction errors'},
        ),
    ]
