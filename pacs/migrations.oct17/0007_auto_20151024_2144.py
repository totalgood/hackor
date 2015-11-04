# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0006_auto_20151024_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawcandidatefilings',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=0, serialize=False, verbose_name='ID'),
            preserve_default=False,
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
            model_name='rawcandidatefilings',
            name='candidate_file_rsn',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
