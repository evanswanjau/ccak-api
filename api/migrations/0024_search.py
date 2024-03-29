# Generated by Django 4.2.1 on 2023-05-30 15:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0023_member_agree_to_terms"),
    ]

    operations = [
        migrations.CreateModel(
            name="Search",
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
                ("keyword", models.CharField(blank=True, max_length=300)),
                ("table", models.CharField(blank=True, max_length=300)),
                ("category", models.CharField(blank=True, max_length=150)),
                ("ip_address", models.CharField(blank=True, max_length=150)),
                ("created_by", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
