# Generated by Django 2.2.13 on 2020-08-21 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0045_auto_20200902_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='upstream_id',
            field=models.CharField(max_length=126, null=True),
        ),
    ]
