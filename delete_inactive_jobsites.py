import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "find_your_dreamjob.settings")

django.setup()

from job_searcher.models import Job, RawJob
from job_searcher.functions.utility.ping_url import ping_url

inactive_jobs = Job.objects.filter(is_active=False)

print(f"Es sind {inactive_jobs.count()} inaktive Jobs in unserer Datenbank.")

for job in inactive_jobs[:5]:
    print(f"{ping_url(job.joblisting_url)}: {job.joblisting_url}")

to_delete = input("Should the not found jobsites be deleted? (y/n)")

clear_answer = False

while clear_answer == False:

    if to_delete == "y":
        inactive_jobs.delete()
        clear_answer = True
    elif to_delete == "n":
        clear_answer = True
    else:
        to_delete = input("Please answer with 'y' or 'n'.")
