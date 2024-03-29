# Generated by Django 4.2.1 on 2023-07-17 07:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0033_administrator_role"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                ("transaction_id", models.CharField(blank=True, max_length=150)),
                ("method", models.CharField(max_length=150)),
                ("invoice_number", models.CharField(max_length=150)),
                ("timestamp", models.CharField(max_length=150)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("paid_by", models.JSONField(default=dict)),
                ("created_by", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("last_updated", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
