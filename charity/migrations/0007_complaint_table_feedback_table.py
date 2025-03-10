# Generated by Django 5.1.3 on 2024-11-30 09:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0006_alter_blockchain_transaction_table_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='complaint_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint_date', models.CharField(max_length=300)),
                ('reply_date', models.CharField(max_length=100)),
                ('complaint', models.CharField(max_length=300)),
                ('reply', models.CharField(max_length=100)),
                ('USER', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='charity.registration_table')),
            ],
        ),
        migrations.CreateModel(
            name='feedback_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.CharField(max_length=300)),
                ('feedback_date', models.CharField(max_length=100)),
                ('rating', models.CharField(default=1, max_length=100)),
                ('USER', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='charity.registration_table')),
            ],
        ),
    ]
