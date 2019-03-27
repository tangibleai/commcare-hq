# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-14 16:51
from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models, ProgrammingError

from corehq.sql_db.migrations import partitioned
from corehq.sql_db.operations import RawSQLMigration

migrator = RawSQLMigration(('corehq', 'blobs', 'sql_templates'), {})


def _drop_empty_default_blobmeta_table(apps, schema_editor):
    """Drop unused table in partitioned environment 'default' database

    The table is only dropped if it is empty (as it should be).
    """
    if schema_editor.connection.alias != "default" or not settings.USE_PARTITIONED_DATABASE:
        return

    with schema_editor.connection.cursor() as cursor:
        try:
            cursor.execute("SELECT COUNT(*) FROM blobs_blobmeta")
        except ProgrammingError as err:
            if '"blobs_blobmeta" does not exist' in repr(err):
                return
        blob_count = cursor.fetchone()[0]
        if blob_count > 0:
            # Unexpected state! Do not drop non-empty table.
            return

        cursor.execute("DROP TABLE blobs_blobmeta;")


class Migration(migrations.Migration):

    dependencies = [
        ('blobs', '0007_drop_blobmeta_view'),
    ]

    operations = [
        partitioned(migrations.CreateModel(
            name='DeletedBlobMeta',
            fields=[
                ('id', models.IntegerField(primary_key=True)),
                ('domain', models.CharField(max_length=255)),
                ('parent_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('key', models.CharField(max_length=255)),
                ('type_code', models.PositiveSmallIntegerField()),
                ('created_on', models.DateTimeField()),
                ('deleted_on', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        )),
        partitioned(
            migrator.get_migration('delete_blob_meta_v2.sql', 'delete_blob_meta.sql'),
            apply_to_proxy=False,
        ),
        migrations.RunPython(_drop_empty_default_blobmeta_table, migrations.RunPython.noop),
    ]
