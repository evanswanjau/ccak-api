# Generated by Django 4.2.1 on 2023-08-24 20:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0052_socialpost_logo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="bookmarks",
            field=models.JSONField(default=[]),
        ),
    ]