# Generated by Django 4.1.4 on 2023-01-07 19:22

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("job_searcher", "0015_alter_userrating_job_remove_userrating_user_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="userrating", unique_together={("job", "user")},
        ),
    ]