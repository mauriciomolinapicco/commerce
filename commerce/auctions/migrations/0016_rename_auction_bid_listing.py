# Generated by Django 5.0.2 on 2024-02-23 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_comment_date_comment_listing_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='auction',
            new_name='listing',
        ),
    ]
