# Generated by Django 4.2.1 on 2023-06-01 19:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0027_subscriber"),
    ]

    operations = [
        migrations.AddField(
            model_name="search",
            name="technology",
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
