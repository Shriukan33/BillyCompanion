# Generated by Django 5.0.2 on 2024-02-22 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
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
                (
                    "title",
                    models.CharField(
                        choices=[
                            ("FDCN", "La Forteresse du Chaudron Noir"),
                            ("CDSI", "La Corne des Sables d'Ivoire"),
                        ],
                        default="FDCN",
                        max_length=500,
                    ),
                ),
                ("chapters_count", models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
