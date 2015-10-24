# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from pacs.management.commands.clean_committee_transactions import \
    clean_duplicate_original_ids_from_raw_committee_transactions
from pacs.models import CommitteeTransactions


def forwards_func(apps, schema_editor):
    clean_duplicate_original_ids_from_raw_committee_transactions()


def reverse_func(apps, schema_editor):
    CommitteeTransactions = apps.get_model("pacs", "CommitteeTransactions")
    CommitteeTransactions.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0003_committeetransactions'),
    ]

    # https://docs.djangoproject.com/en/1.8/ref/migration-operations/#runpython
    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]
