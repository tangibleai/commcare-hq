# Generated by Django 1.10.7 on 2017-05-11 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('icds_reports', '0015_add_aggregation_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggAwcMonthly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('awc_id', models.TextField(blank=True, null=True)),
                ('awc_name', models.TextField(blank=True, null=True)),
                ('awc_site_code', models.TextField(blank=True, null=True)),
                ('supervisor_id', models.TextField(blank=True, null=True)),
                ('supervisor_name', models.TextField(blank=True, null=True)),
                ('supervisor_site_code', models.TextField(blank=True, null=True)),
                ('block_id', models.TextField(blank=True, null=True)),
                ('block_name', models.TextField(blank=True, null=True)),
                ('block_site_code', models.TextField(blank=True, null=True)),
                ('district_id', models.TextField(blank=True, null=True)),
                ('district_name', models.TextField(blank=True, null=True)),
                ('district_site_code', models.TextField(blank=True, null=True)),
                ('state_id', models.TextField(blank=True, null=True)),
                ('state_name', models.TextField(blank=True, null=True)),
                ('state_site_code', models.TextField(blank=True, null=True)),
                ('aggregation_level', models.IntegerField(blank=True, null=True)),
                ('month', models.DateField(blank=True, null=True)),
                ('is_launched', models.TextField(blank=True, null=True)),
                ('num_awcs', models.IntegerField(blank=True, null=True)),
                ('awc_days_open', models.IntegerField(blank=True, null=True)),
                ('total_eligible_children', models.IntegerField(blank=True, null=True)),
                ('total_attended_children', models.IntegerField(blank=True, null=True)),
                ('pse_avg_attendance_percent', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('pse_full', models.IntegerField(blank=True, null=True)),
                ('pse_partial', models.IntegerField(blank=True, null=True)),
                ('pse_non', models.IntegerField(blank=True, null=True)),
                ('pse_score', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('awc_days_provided_breakfast', models.IntegerField(blank=True, null=True)),
                ('awc_days_provided_hotmeal', models.IntegerField(blank=True, null=True)),
                ('awc_days_provided_thr', models.IntegerField(blank=True, null=True)),
                ('awc_days_provided_pse', models.IntegerField(blank=True, null=True)),
                ('awc_not_open_holiday', models.IntegerField(blank=True, null=True)),
                ('awc_not_open_festival', models.IntegerField(blank=True, null=True)),
                ('awc_not_open_no_help', models.IntegerField(blank=True, null=True)),
                ('awc_not_open_department_work', models.IntegerField(blank=True, null=True)),
                ('awc_not_open_other', models.IntegerField(blank=True, null=True)),
                ('awc_num_open', models.IntegerField(blank=True, null=True)),
                ('awc_not_open_no_data', models.IntegerField(blank=True, null=True)),
                ('wer_weighed', models.IntegerField(blank=True, null=True)),
                ('wer_eligible', models.IntegerField(blank=True, null=True)),
                ('wer_score', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('thr_eligible_child', models.IntegerField(blank=True, null=True)),
                ('thr_rations_21_plus_distributed_child', models.IntegerField(blank=True, null=True)),
                ('thr_eligible_ccs', models.IntegerField(blank=True, null=True)),
                ('thr_rations_21_plus_distributed_ccs', models.IntegerField(blank=True, null=True)),
                ('thr_score', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('awc_score', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('num_awc_rank_functional', models.IntegerField(blank=True, null=True)),
                ('num_awc_rank_semi', models.IntegerField(blank=True, null=True)),
                ('num_awc_rank_non', models.IntegerField(blank=True, null=True)),
                ('cases_ccs_pregnant', models.IntegerField(blank=True, null=True)),
                ('cases_ccs_lactating', models.IntegerField(blank=True, null=True)),
                ('cases_child_health', models.IntegerField(blank=True, null=True)),
                ('usage_num_pse', models.IntegerField(blank=True, null=True)),
                ('usage_num_gmp', models.IntegerField(blank=True, null=True)),
                ('usage_num_thr', models.IntegerField(blank=True, null=True)),
                ('usage_num_home_visit', models.IntegerField(blank=True, null=True)),
                ('usage_num_bp_tri1', models.IntegerField(blank=True, null=True)),
                ('usage_num_bp_tri2', models.IntegerField(blank=True, null=True)),
                ('usage_num_bp_tri3', models.IntegerField(blank=True, null=True)),
                ('usage_num_pnc', models.IntegerField(blank=True, null=True)),
                ('usage_num_ebf', models.IntegerField(blank=True, null=True)),
                ('usage_num_cf', models.IntegerField(blank=True, null=True)),
                ('usage_num_delivery', models.IntegerField(blank=True, null=True)),
                ('usage_num_due_list_ccs', models.IntegerField(blank=True, null=True)),
                ('usage_num_due_list_child_health', models.IntegerField(blank=True, null=True)),
                ('usage_awc_num_active', models.IntegerField(blank=True, null=True)),
                ('usage_time_pse', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('usage_time_gmp', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('usage_time_bp', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('usage_time_pnc', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('usage_time_ebf', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('usage_time_cf', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('usage_time_of_day_pse', models.TimeField(blank=True, null=True)),
                ('usage_time_of_day_home_visit', models.TimeField(blank=True, null=True)),
                ('vhnd_immunization', models.IntegerField(blank=True, null=True)),
                ('vhnd_anc', models.IntegerField(blank=True, null=True)),
                ('vhnd_gmp', models.IntegerField(blank=True, null=True)),
                ('vhnd_num_pregnancy', models.IntegerField(blank=True, null=True)),
                ('vhnd_num_lactating', models.IntegerField(blank=True, null=True)),
                ('vhnd_num_mothers_6_12', models.IntegerField(blank=True, null=True)),
                ('vhnd_num_mothers_12', models.IntegerField(blank=True, null=True)),
                ('vhnd_num_fathers', models.IntegerField(blank=True, null=True)),
                ('ls_supervision_visit', models.IntegerField(blank=True, null=True)),
                ('ls_num_supervised', models.IntegerField(blank=True, null=True)),
                ('ls_awc_location_long', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('ls_awc_location_lat', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('ls_awc_present', models.IntegerField(blank=True, null=True)),
                ('ls_awc_open', models.IntegerField(blank=True, null=True)),
                ('ls_awc_not_open_aww_not_available', models.IntegerField(blank=True, null=True)),
                ('ls_awc_not_open_closed_early', models.IntegerField(blank=True, null=True)),
                ('ls_awc_not_open_holiday', models.IntegerField(blank=True, null=True)),
                ('ls_awc_not_open_unknown', models.IntegerField(blank=True, null=True)),
                ('ls_awc_not_open_other', models.IntegerField(blank=True, null=True)),
                ('infra_last_update_date', models.DateField(blank=True, null=True)),
                ('infra_type_of_building', models.TextField(blank=True, null=True)),
                ('infra_type_of_building_pucca', models.IntegerField(blank=True, null=True)),
                ('infra_type_of_building_semi_pucca', models.IntegerField(blank=True, null=True)),
                ('infra_type_of_building_kuccha', models.IntegerField(blank=True, null=True)),
                ('infra_type_of_building_partial_covered_space', models.IntegerField(blank=True, null=True)),
                ('infra_clean_water', models.IntegerField(blank=True, null=True)),
                ('infra_functional_toilet', models.IntegerField(blank=True, null=True)),
                ('infra_baby_weighing_scale', models.IntegerField(blank=True, null=True)),
                ('infra_flat_weighing_scale', models.IntegerField(blank=True, null=True)),
                ('infra_adult_weighing_scale', models.IntegerField(blank=True, null=True)),
                ('infra_cooking_utensils', models.IntegerField(blank=True, null=True)),
                ('infra_medicine_kits', models.IntegerField(blank=True, null=True)),
                ('infra_adequate_space_pse', models.IntegerField(blank=True, null=True)),
                ('usage_num_hh_reg', models.IntegerField(blank=True, null=True)),
                ('usage_num_add_person', models.IntegerField(blank=True, null=True)),
                ('usage_num_add_pregnancy', models.IntegerField(blank=True, null=True)),
                ('training_phase', models.IntegerField(blank=True, null=True)),
                ('trained_phase_1', models.IntegerField(blank=True, null=True)),
                ('trained_phase_2', models.IntegerField(blank=True, null=True)),
                ('trained_phase_3', models.IntegerField(blank=True, null=True)),
                ('trained_phase_4', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'agg_awc_monthly',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AggCcsRecordMonthly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('awc_id', models.TextField(blank=True, null=True)),
                ('awc_name', models.TextField(blank=True, null=True)),
                ('awc_site_code', models.TextField(blank=True, null=True)),
                ('supervisor_id', models.TextField(blank=True, null=True)),
                ('supervisor_name', models.TextField(blank=True, null=True)),
                ('supervisor_site_code', models.TextField(blank=True, null=True)),
                ('block_id', models.TextField(blank=True, null=True)),
                ('block_name', models.TextField(blank=True, null=True)),
                ('block_site_code', models.TextField(blank=True, null=True)),
                ('district_id', models.TextField(blank=True, null=True)),
                ('district_name', models.TextField(blank=True, null=True)),
                ('district_site_code', models.TextField(blank=True, null=True)),
                ('state_id', models.TextField(blank=True, null=True)),
                ('state_name', models.TextField(blank=True, null=True)),
                ('state_site_code', models.TextField(blank=True, null=True)),
                ('aggregation_level', models.IntegerField(blank=True, null=True)),
                ('month', models.DateField(blank=True, null=True)),
                ('ccs_status', models.TextField(blank=True, null=True)),
                ('trimester', models.TextField(blank=True, null=True)),
                ('caste', models.TextField(blank=True, null=True)),
                ('disabled', models.TextField(blank=True, null=True)),
                ('minority', models.TextField(blank=True, null=True)),
                ('resident', models.TextField(blank=True, null=True)),
                ('valid_in_month', models.IntegerField(blank=True, null=True)),
                ('lactating', models.IntegerField(blank=True, null=True)),
                ('pregnant', models.IntegerField(blank=True, null=True)),
                ('thr_eligible', models.IntegerField(blank=True, null=True)),
                ('rations_21_plus_distributed', models.IntegerField(blank=True, null=True)),
                ('tetanus_complete', models.IntegerField(blank=True, null=True)),
                ('delivered_in_month', models.IntegerField(blank=True, null=True)),
                ('anc1_received_at_delivery', models.IntegerField(blank=True, null=True)),
                ('anc2_received_at_delivery', models.IntegerField(blank=True, null=True)),
                ('anc3_received_at_delivery', models.IntegerField(blank=True, null=True)),
                ('anc4_received_at_delivery', models.IntegerField(blank=True, null=True)),
                ('registration_trimester_at_delivery', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('using_ifa', models.IntegerField(blank=True, null=True)),
                ('ifa_consumed_last_seven_days', models.IntegerField(blank=True, null=True)),
                ('anemic_normal', models.IntegerField(blank=True, null=True)),
                ('anemic_moderate', models.IntegerField(blank=True, null=True)),
                ('anemic_severe', models.IntegerField(blank=True, null=True)),
                ('anemic_unknown', models.IntegerField(blank=True, null=True)),
                ('extra_meal', models.IntegerField(blank=True, null=True)),
                ('resting_during_pregnancy', models.IntegerField(blank=True, null=True)),
                ('bp1_complete', models.IntegerField(blank=True, null=True)),
                ('bp2_complete', models.IntegerField(blank=True, null=True)),
                ('bp3_complete', models.IntegerField(blank=True, null=True)),
                ('pnc_complete', models.IntegerField(blank=True, null=True)),
                ('trimester_2', models.IntegerField(blank=True, null=True)),
                ('trimester_3', models.IntegerField(blank=True, null=True)),
                ('postnatal', models.IntegerField(blank=True, null=True)),
                ('counsel_bp_vid', models.IntegerField(blank=True, null=True)),
                ('counsel_preparation', models.IntegerField(blank=True, null=True)),
                ('counsel_immediate_bf', models.IntegerField(blank=True, null=True)),
                ('counsel_fp_vid', models.IntegerField(blank=True, null=True)),
                ('counsel_immediate_conception', models.IntegerField(blank=True, null=True)),
                ('counsel_accessible_postpartum_fp', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'agg_ccs_record_monthly',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AggChildHealthMonthly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('awc_id', models.TextField(blank=True, null=True)),
                ('awc_name', models.TextField(blank=True, null=True)),
                ('awc_site_code', models.TextField(blank=True, null=True)),
                ('supervisor_id', models.TextField(blank=True, null=True)),
                ('supervisor_name', models.TextField(blank=True, null=True)),
                ('supervisor_site_code', models.TextField(blank=True, null=True)),
                ('block_id', models.TextField(blank=True, null=True)),
                ('block_name', models.TextField(blank=True, null=True)),
                ('block_site_code', models.TextField(blank=True, null=True)),
                ('district_id', models.TextField(blank=True, null=True)),
                ('district_name', models.TextField(blank=True, null=True)),
                ('district_site_code', models.TextField(blank=True, null=True)),
                ('state_id', models.TextField(blank=True, null=True)),
                ('state_name', models.TextField(blank=True, null=True)),
                ('state_site_code', models.TextField(blank=True, null=True)),
                ('aggregation_level', models.IntegerField(blank=True, null=True)),
                ('month', models.DateField(blank=True, null=True)),
                ('month_display', models.TextField(blank=True, null=True)),
                ('gender', models.TextField(blank=True, null=True)),
                ('age_tranche', models.TextField(blank=True, null=True)),
                ('caste', models.TextField(blank=True, null=True)),
                ('disabled', models.TextField(blank=True, null=True)),
                ('minority', models.TextField(blank=True, null=True)),
                ('resident', models.TextField(blank=True, null=True)),
                ('valid_in_month', models.IntegerField(blank=True, null=True)),
                ('nutrition_status_weighed', models.IntegerField(blank=True, null=True)),
                ('nutrition_status_unweighed', models.IntegerField(blank=True, null=True)),
                ('nutrition_status_normal', models.IntegerField(blank=True, null=True)),
                ('nutrition_status_moderately_underweight', models.IntegerField(blank=True, null=True)),
                ('nutrition_status_severely_underweight', models.IntegerField(blank=True, null=True)),
                ('wer_eligible', models.IntegerField(blank=True, null=True)),
                ('thr_eligible', models.IntegerField(blank=True, null=True)),
                ('rations_21_plus_distributed', models.IntegerField(blank=True, null=True)),
                ('pse_eligible', models.IntegerField(blank=True, null=True)),
                ('pse_attended_16_days', models.IntegerField(blank=True, null=True)),
                ('born_in_month', models.IntegerField(blank=True, null=True)),
                ('low_birth_weight_in_month', models.IntegerField(blank=True, null=True)),
                ('bf_at_birth', models.IntegerField(blank=True, null=True)),
                ('ebf_eligible', models.IntegerField(blank=True, null=True)),
                ('ebf_in_month', models.IntegerField(blank=True, null=True)),
                ('cf_eligible', models.IntegerField(blank=True, null=True)),
                ('cf_in_month', models.IntegerField(blank=True, null=True)),
                ('cf_diet_diversity', models.IntegerField(blank=True, null=True)),
                ('cf_diet_quantity', models.IntegerField(blank=True, null=True)),
                ('cf_demo', models.IntegerField(blank=True, null=True)),
                ('cf_handwashing', models.IntegerField(blank=True, null=True)),
                ('counsel_increase_food_bf', models.IntegerField(blank=True, null=True)),
                ('counsel_manage_breast_problems', models.IntegerField(blank=True, null=True)),
                ('counsel_ebf', models.IntegerField(blank=True, null=True)),
                ('counsel_adequate_bf', models.IntegerField(blank=True, null=True)),
                ('counsel_pediatric_ifa', models.IntegerField(blank=True, null=True)),
                ('counsel_play_cf_video', models.IntegerField(blank=True, null=True)),
                ('fully_immunized_eligible', models.IntegerField(blank=True, null=True)),
                ('fully_immunized_on_time', models.IntegerField(blank=True, null=True)),
                ('fully_immunized_late', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'agg_child_health_monthly',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AggDailyUsageView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('awc_id', models.TextField(blank=True, null=True)),
                ('awc_name', models.TextField(blank=True, null=True)),
                ('awc_site_code', models.TextField(blank=True, null=True)),
                ('supervisor_id', models.TextField(blank=True, null=True)),
                ('supervisor_name', models.TextField(blank=True, null=True)),
                ('supervisor_site_code', models.TextField(blank=True, null=True)),
                ('block_id', models.TextField(blank=True, null=True)),
                ('block_name', models.TextField(blank=True, null=True)),
                ('block_site_code', models.TextField(blank=True, null=True)),
                ('district_id', models.TextField(blank=True, null=True)),
                ('district_name', models.TextField(blank=True, null=True)),
                ('district_site_code', models.TextField(blank=True, null=True)),
                ('state_id', models.TextField(blank=True, null=True)),
                ('state_name', models.TextField(blank=True, null=True)),
                ('state_site_code', models.TextField(blank=True, null=True)),
                ('aggregation_level', models.IntegerField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('daily_attendance_open', models.IntegerField(blank=True, null=True)),
                ('usage_num_forms', models.IntegerField(blank=True, null=True)),
                ('usage_num_home_visit', models.IntegerField(blank=True, null=True)),
                ('usage_num_gmp', models.IntegerField(blank=True, null=True)),
                ('usage_num_thr', models.IntegerField(blank=True, null=True)),
                ('awc_count', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'agg_daily_usage_view',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AggThrMonthly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('awc_id', models.TextField(blank=True, null=True)),
                ('awc_name', models.TextField(blank=True, null=True)),
                ('awc_site_code', models.TextField(blank=True, null=True)),
                ('supervisor_id', models.TextField(blank=True, null=True)),
                ('supervisor_name', models.TextField(blank=True, null=True)),
                ('supervisor_site_code', models.TextField(blank=True, null=True)),
                ('block_id', models.TextField(blank=True, null=True)),
                ('block_name', models.TextField(blank=True, null=True)),
                ('block_site_code', models.TextField(blank=True, null=True)),
                ('district_id', models.TextField(blank=True, null=True)),
                ('district_name', models.TextField(blank=True, null=True)),
                ('district_site_code', models.TextField(blank=True, null=True)),
                ('state_id', models.TextField(blank=True, null=True)),
                ('state_name', models.TextField(blank=True, null=True)),
                ('state_site_code', models.TextField(blank=True, null=True)),
                ('aggregation_level', models.IntegerField(blank=True, null=True)),
                ('month', models.DateField(blank=True, null=True)),
                ('beneficiary_type', models.TextField(blank=True, null=True)),
                ('caste', models.TextField(blank=True, null=True)),
                ('disabled', models.TextField(blank=True, null=True)),
                ('minority', models.TextField(blank=True, null=True)),
                ('resident', models.TextField(blank=True, null=True)),
                ('thr_eligible', models.IntegerField(blank=True, null=True)),
                ('rations_21_plus_distributed', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'agg_thr_monthly',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AwcLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_id', models.TextField()),
                ('awc_name', models.TextField(blank=True, null=True)),
                ('awc_site_code', models.TextField(blank=True, null=True)),
                ('supervisor_id', models.TextField()),
                ('supervisor_name', models.TextField(blank=True, null=True)),
                ('supervisor_site_code', models.TextField(blank=True, null=True)),
                ('block_id', models.TextField()),
                ('block_name', models.TextField(blank=True, null=True)),
                ('block_site_code', models.TextField(blank=True, null=True)),
                ('district_id', models.TextField()),
                ('district_name', models.TextField(blank=True, null=True)),
                ('district_site_code', models.TextField(blank=True, null=True)),
                ('state_id', models.TextField()),
                ('state_name', models.TextField(blank=True, null=True)),
                ('state_site_code', models.TextField(blank=True, null=True)),
                ('aggregation_level', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'awc_location',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AwcLocationMonths',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('awc_id', models.TextField(blank=True, null=True)),
                ('awc_name', models.TextField(blank=True, null=True)),
                ('awc_site_code', models.TextField(blank=True, null=True)),
                ('supervisor_id', models.TextField(blank=True, null=True)),
                ('supervisor_name', models.TextField(blank=True, null=True)),
                ('supervisor_site_code', models.TextField(blank=True, null=True)),
                ('block_id', models.TextField(blank=True, null=True)),
                ('block_name', models.TextField(blank=True, null=True)),
                ('block_site_code', models.TextField(blank=True, null=True)),
                ('district_id', models.TextField(blank=True, null=True)),
                ('district_name', models.TextField(blank=True, null=True)),
                ('district_site_code', models.TextField(blank=True, null=True)),
                ('state_id', models.TextField(blank=True, null=True)),
                ('state_name', models.TextField(blank=True, null=True)),
                ('state_site_code', models.TextField(blank=True, null=True)),
                ('aggregation_level', models.IntegerField(blank=True, null=True)),
                ('month', models.DateField(blank=True, null=True)),
                ('month_display', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'awc_location_months',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DailyAttendanceView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('awc_id', models.TextField(blank=True, null=True)),
                ('awc_name', models.TextField(blank=True, null=True)),
                ('awc_site_code', models.TextField(blank=True, null=True)),
                ('supervisor_id', models.TextField(blank=True, null=True)),
                ('supervisor_name', models.TextField(blank=True, null=True)),
                ('supervisor_site_code', models.TextField(blank=True, null=True)),
                ('block_id', models.TextField(blank=True, null=True)),
                ('block_name', models.TextField(blank=True, null=True)),
                ('block_site_code', models.TextField(blank=True, null=True)),
                ('district_id', models.TextField(blank=True, null=True)),
                ('district_name', models.TextField(blank=True, null=True)),
                ('district_site_code', models.TextField(blank=True, null=True)),
                ('state_id', models.TextField(blank=True, null=True)),
                ('state_name', models.TextField(blank=True, null=True)),
                ('state_site_code', models.TextField(blank=True, null=True)),
                ('aggregation_level', models.IntegerField(blank=True, null=True)),
                ('month', models.DateField(blank=True, null=True)),
                ('doc_id', models.TextField(blank=True, null=True)),
                ('pse_date', models.DateField(blank=True, null=True)),
                ('awc_open_count', models.IntegerField(blank=True, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('eligible_children', models.IntegerField(blank=True, null=True)),
                ('attended_children', models.IntegerField(blank=True, null=True)),
                ('attended_children_percent', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('form_location', models.TextField(blank=True, null=True)),
                ('form_location_lat', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('form_location_long', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('image_name', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'daily_attendance_view',
                'managed': False,
            },
        ),
    ]