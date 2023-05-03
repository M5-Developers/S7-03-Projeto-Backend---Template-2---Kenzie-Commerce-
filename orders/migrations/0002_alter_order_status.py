# Generated by Django 4.2 on 2023-05-03 15:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("In progress", "Inprogress"),
                    ("Delivered", "Delivered"),
                ],
                default="Pending",
                max_length=20,
            ),
        ),
    ]
