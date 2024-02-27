# Generated by Django 4.2.1 on 2024-02-27 23:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0058_alter_socialpost_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="Content",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("page", models.CharField(max_length=150)),
                ("section", models.IntegerField(default=150)),
                ("content", models.JSONField(default=dict)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("last_updated", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
