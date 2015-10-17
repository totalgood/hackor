# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pacs.models


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0002_auto_20151017_0621'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommitteeTransactions',
            fields=[
                ('tran_id', models.IntegerField(serialize=False, primary_key=True, blank=True)),
                ('original_id', models.IntegerField(blank=True)),
                ('tran_date', models.DateField(null=True, blank=True)),
                ('tran_status', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('filer', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('contributor_payee', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('sub_type', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('amount', models.FloatField(null=True, blank=True)),
                ('aggregate_amount', models.FloatField(null=True, blank=True)),
                ('contributor_payee_committee_id', models.IntegerField(null=True, blank=True)),
                ('filer_id', models.IntegerField(null=True, blank=True)),
                ('attest_by_name', pacs.models.LongCharField(max_length=1000000000)),
                ('attest_date', models.DateField()),
                ('review_by_name', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('review_date', models.DateField(null=True, blank=True)),
                ('due_date', models.DateField(null=True, blank=True)),
                ('occptn_ltr_date', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('pymt_sched_txt', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('purp_desc', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('intrst_rate', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('check_nbr', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('tran_stsfd_ind', models.NullBooleanField()),
                ('filed_by_name', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('filed_date', models.DateField(null=True, blank=True)),
                ('addr_book_agent_name', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('book_type', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('title_txt', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('occptn_txt', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('emp_name', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('emp_city', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('emp_state', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('employ_ind', models.NullBooleanField()),
                ('self_employ_ind', models.NullBooleanField()),
                ('addr_line1', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('addr_line2', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('city', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('state', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('zip', models.IntegerField(null=True, blank=True)),
                ('zip_plus_four', models.IntegerField(null=True, blank=True)),
                ('county', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('purpose_codes', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
                ('exp_date', pacs.models.LongCharField(max_length=1000000000, null=True, blank=True)),
            ],
        ),
    ]
