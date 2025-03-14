# Generated by Django 5.1 on 2025-02-06 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0011_remove_donation_donor_name_donation_charity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_address', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=5, max_digits=10)),
                ('transaction_hash', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='donation',
            name='charity',
        ),
        migrations.DeleteModel(
            name='blockchain_transaction_table',
        ),
        migrations.DeleteModel(
            name='Donation',
        ),
    ]
