# Generated by Django 4.2.1 on 2023-07-03 07:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0030_kopokopo_alter_invoice_invoice_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="tags",
            field=models.JSONField(default=dict),
        ),
    ]
