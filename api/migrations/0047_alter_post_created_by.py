# Generated by Django 4.2.1 on 2023-08-20 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0046_alter_payment_invoice_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                default=1,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_created",
                to="api.administrator",
            ),
        ),
    ]