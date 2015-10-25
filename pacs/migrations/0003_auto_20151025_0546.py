# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0002_auto_20151025_0544'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ccgrassrootsinstate',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='ccworkingtransactions',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='directioncodes',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='documentation',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='hackoregondbstatus',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='importdates',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='oregonbycontributions',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='oregonbypurposecodes',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='oregoncommitteeagg',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='pacscommitteetransactions',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='rawcandidatefilings',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='rawcommittees',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='rawcommitteesscraped',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='rawcommitteetransactions',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='rawcommitteetransactionsammendedtransactions',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='rawcommitteetransactionserrors',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='searchlog',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='statesumbydate',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='statetranslation',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='subtypefromcontributorpayee',
            options={'managed': True},
        ),
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
