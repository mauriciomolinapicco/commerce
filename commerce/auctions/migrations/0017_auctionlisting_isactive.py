# Generated by Django 5.0.2 on 2024-02-23 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_rename_auction_bid_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]