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
            name='AccessLogUpdate',
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
        migrations.AlterModelOptions(
            name='campaigndetail',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='rawcandidatefilings',
            options={'managed': True, 'verbose_name': 'candidate filing'},
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
            field=models.IntegerField(default=0, serialize=False, primary_key=True),
        ),
    ]
