# Generated by Django 4.1.4 on 2022-12-22 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job_searcher", "0009_job_language_rawjob_language"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserRequests",
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
                    "key_words",
                    models.ManyToManyField(blank=True, to="job_searcher.keyword"),
                ),
                (
                    "search_terms",
                    models.ManyToManyField(blank=True, to="job_searcher.searchterm"),
                ),
            ],
        ),
    ]
