import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "find_your_dreamjob.settings")

django.setup()

from job_searcher.models import Job, RawJob

#Jobs with no Job Location
""" no_job_location = RawJob.objects.filter(job_location__isnull=True)
print(no_job_location) """


#Jobs who are only in RawJob
""" rawjob_ids = RawJob.objects.values_list('joblisting_url', flat=True)
job_ids = Job.objects.values_list('joblisting_url', flat=True)

print(set.difference(set(rawjob_ids), set(job_ids))) """