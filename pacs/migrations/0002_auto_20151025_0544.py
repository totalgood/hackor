# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accesslog',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='acgrassrootsinstate',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='alloregonsum',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='campaigndetail',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='candidatebystate',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='candidatesumbydate',
            options={'managed': True},
        ),
    ]
