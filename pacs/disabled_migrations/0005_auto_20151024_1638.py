# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0004_auto_20151024_1628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='importdates',
            name='id',
        ),
        migrations.RemoveField(
            model_name='rawcommitteesscraped',
            name='id',
        ),
        migrations.AddField(
            model_name='importdates',
            name='file_hash',
            field=models.DecimalField(primary_key=True, db_column='id', default=0, serialize=False, decimal_places=65535, max_digits=65535, blank=True),
        ),
        migrations.AddField(
            model_name='rawcommitteesscraped',
            name='committee_id',
            field=models.IntegerField(default=0, serialize=False, primary_key=True, db_column='id', blank=True),
        ),
        migrations.AlterField(
            model_name='campaigndetail',
            name='candidate_name',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='campaigndetail',
            name='filer_id',
            field=models.IntegerField(default=0, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='committeetransactions',
            name='tran_id',
            field=models.IntegerField(default=0, serialize=False, primary_key=True, blank=True),
        ),
        migrations.AlterField(
            model_name='rawcommitteetransactions',
            name='tran_id',
            field=models.IntegerField(default=0, serialize=False, primary_key=True),
        ),
    ]
