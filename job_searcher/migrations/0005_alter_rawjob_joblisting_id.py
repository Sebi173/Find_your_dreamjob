# Generated by Django 4.1.3 on 2022-12-21 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job_searcher", "0004_alter_rawjob_company_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rawjob",
            name="joblisting_id",
            field=models.IntegerField(null=True),
        ),
    ]