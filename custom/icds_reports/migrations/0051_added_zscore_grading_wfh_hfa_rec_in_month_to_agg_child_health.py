# Generated by Django 1.11.12 on 2018-06-06 12:57

from django.db import migrations, models

from corehq.sql_db.operations import RawSQLMigration

migrator = RawSQLMigration(('custom', 'icds_reports', 'migrations', 'sql_templates'))


class Migration(migrations.Migration):

    dependencies = [
        ('icds_reports', '0050_move_to_django'),
    ]

    operations = [
        migrator.get_migration('update_tables23.sql'),

        migrations.AddField(
            model_name='AggChildHealth',
            name='zscore_grading_hfa_recorded_in_month',
            field=models.IntegerField(blank=True, null=True)
        ),
        migrations.AddField(
            model_name='AggChildHealth',
            name='zscore_grading_wfh_recorded_in_month',
            field=models.IntegerField(blank=True, null=True)
        )
    ]