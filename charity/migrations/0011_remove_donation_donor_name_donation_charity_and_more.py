# Generated by Django 5.1 on 2025-02-04 10:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0010_donation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donation',
            name='donor_name',
        ),
        migrations.AddField(
            model_name='donation',
            name='charity',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='charity.charity_table'),
        ),
        migrations.AddField(
            model_name='donation',
            name='donor_address',
            field=models.CharField(default=1, max_length=255),
        ),
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.AlterField(
            model_name='donation',
            name='transaction_hash',
            field=models.CharField(max_length=255),
        ),
    ]
