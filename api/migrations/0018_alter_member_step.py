# Generated by Django 4.2.1 on 2023-05-16 14:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0017_member"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="step",
            field=models.CharField(blank=True, max_length=150),
        ),
    ]