# Generated by Django 5.0.2 on 2024-02-24 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_auctionlisting_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='numberOfBids',
            field=models.IntegerField(default=0),
        ),
    ]
