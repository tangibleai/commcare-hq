# Generated by Django 1.11.16 on 2018-10-26 19:14

from django.db import migrations


class Migration(migrations.Migration):

    # this migration requires those views to be generated
    # yet it shouldn't include more to allow adding columns to other views
    dependencies = [
        ('icds_reports', '0070_aww_name_in_agg_ccs_view'),
    ]
    operations = []