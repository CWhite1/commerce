# Generated by Django 4.1.3 on 2022-12-27 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bids',
            name='bid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True),
        ),
    ]
