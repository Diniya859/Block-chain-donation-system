# Generated by Django 5.1.3 on 2024-11-29 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0004_charity_table_blockchain_transaction_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockchain_transaction_table',
            name='amount',
            field=models.BigIntegerField(max_length=99999999),
        ),
    ]
