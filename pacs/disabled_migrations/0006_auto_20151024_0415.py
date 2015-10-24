# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pacs.model_utils


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0005_auto_20151017_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLogs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'access_logs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AllOregonSum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('in_field', models.FloatField(null=True, db_column='in', blank=True)),
                ('out', models.FloatField(null=True, blank=True)),
                ('from_within', models.FloatField(null=True, blank=True)),
                ('to_within', models.FloatField(null=True, blank=True)),
                ('from_outside', models.FloatField(null=True, blank=True)),
                ('to_outside', models.FloatField(null=True, blank=True)),
                ('total_grass_roots', models.FloatField(null=True, blank=True)),
                ('total_from_in_state', models.FloatField(null=True, blank=True)),
            ],
            options={
                'db_table': 'all_oregon_sum',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AllOregonSums',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'all_oregon_sums',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CampaignDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'campaign_details',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CandidateByStates',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'candidate_by_states',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CandidateSumByDates',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'candidate_sum_by_dates',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CcGrassRootsInStates',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'cc_grass_roots_in_states',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SchemaMigrations',
            fields=[
                ('version', pacs.model_utils.LongCharField(max_length=1000000000, unique=True, serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'schema_migrations',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='campaigndetail',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='candidatebystate',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='candidatesumbydate',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='ccgrassrootsinstate',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='ccworkingtransactions',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='directioncodes',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='documentation',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='hackoregondbstatus',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='importdates',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='oregonbycontributions',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='oregonbypurposecodes',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='oregoncommitteeagg',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='rawcandidatefilings',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='rawcommittees',
            options={'managed': False},
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
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='rawcommitteetransactionserrors',
            options={'managed': False},
        ),
        migrations.AlterField(
            model_name='rawcommitteetransactions',
            name='attest_by_name',
            field=pacs.model_utils.LongCharField(max_length=1000000000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='rawcommitteetransactions',
            name='attest_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='rawcommitteetransactions',
            name='original_id',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='rawcommitteetransactions',
            name='tran_id',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
    ]
