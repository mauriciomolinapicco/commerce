# Generated by Django 5.0.2 on 2024-02-21 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlisting_bid_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionlisting',
            old_name='product_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='auctionlisting',
            old_name='product_name',
            new_name='title',
        ),
    ]