# Generated by Django 5.1.3 on 2024-11-29 09:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0003_registration_table_first_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='charity_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='blockchain_transaction_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateTimeField(null=True)),
                ('amount', models.BigIntegerField(max_length=9999999)),
                ('Login', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charity.login_table')),
            ],
        ),
    ]
