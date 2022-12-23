# Generated by Django 4.1.3 on 2022-12-21 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job_searcher", "0002_alter_rawjob_joblisting_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job", name="joblisting_id", field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="job",
            name="key_word",
            field=models.ManyToManyField(blank=True, to="job_searcher.keyword"),
        ),
        migrations.AlterField(
            model_name="job",
            name="search_terms",
            field=models.ManyToManyField(blank=True, to="job_searcher.searchterm"),
        ),
    ]