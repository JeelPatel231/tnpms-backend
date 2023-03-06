# Generated by Django 4.1.2 on 2023-03-06 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("company", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OffCampusPlacedDetail",
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
                ("ctc_lpa", models.FloatField()),
                ("offer_letter", models.FileField(upload_to="offerletters")),
                ("company", models.CharField(max_length=256)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OnCampusPlacedDetail",
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
                ("ctc_lpa", models.FloatField()),
                ("offer_letter", models.FileField(upload_to="offerletters")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="StudentOpening",
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
                ("applied", models.BooleanField(default=False)),
                ("present", models.BooleanField(default=False)),
                ("first_round", models.BooleanField(default=False)),
                ("second_round", models.BooleanField(default=False)),
                ("third_round", models.BooleanField(default=False)),
                ("selected", models.BooleanField(default=False)),
                (
                    "opening",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="company.currentopening",
                    ),
                ),
            ],
            options={
                "verbose_name": "Student Opening",
                "verbose_name_plural": "Student Openings",
            },
        ),
    ]