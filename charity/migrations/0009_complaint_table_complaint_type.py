# Generated by Django 5.1 on 2025-01-08 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0008_rename_first_name_registration_table_fname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint_table',
            name='complaint_type',
            field=models.CharField(default='General', max_length=255),
        ),
    ]
