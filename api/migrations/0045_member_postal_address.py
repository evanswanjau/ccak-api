# Generated by Django 4.2.1 on 2023-08-18 11:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0044_administrator_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="member",
            name="postal_address",
            field=models.CharField(blank=True, max_length=300),
        ),
    ]