# Generated by Django 4.1.4 on 2022-12-21 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job_searcher", "0008_rename_key_word_job_key_words_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="language",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="rawjob",
            name="language",
            field=models.CharField(max_length=50, null=True),
        ),
    ]