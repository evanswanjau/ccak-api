# Generated by Django 4.2.1 on 2023-05-30 15:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0024_search"),
    ]

    operations = [
        migrations.AddField(
            model_name="search",
            name="limit",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="search",
            name="page",
            field=models.IntegerField(default=0),
        ),
    ]