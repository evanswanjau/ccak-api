# Generated by Django 4.2.1 on 2023-06-15 11:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0028_search_technology"),
    ]

    operations = [
        migrations.CreateModel(
            name="Invoice",
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
                ("invoice_number", models.CharField(max_length=50)),
                ("description", models.TextField(blank=True)),
                ("items", models.JSONField(default=dict)),
                ("status", models.CharField(default="unpaid", max_length=150)),
                ("member_id", models.IntegerField(default=0)),
                ("customer", models.JSONField(default=dict)),
                ("created_by", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("last_updated", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]