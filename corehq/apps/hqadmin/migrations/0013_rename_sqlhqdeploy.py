# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-01-31 20:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hqadmin', '0012_remove_sqlhqdeploy_couch_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SQLHqDeploy',
            new_name='HqDeploy',
        ),
        migrations.AlterModelTable(
            name='hqdeploy',
            table=None,
        ),
    ]
