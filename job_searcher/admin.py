from django.contrib import admin

# Register your models here.

from .models import Job, KeyWord, RawJob, SearchTerm, UserRating, UserRequest

class JobAdmin(admin.ModelAdmin):
    list_display = ("job_title", "company", "job_location", "first_crawling_date", "last_crawling_date",)
    list_filter = ("search_terms", "job_location", "company", )
    search_fields = ['job_title', 'company', ]

admin.site.register(Job, JobAdmin)
admin.site.register(KeyWord)
admin.site.register(RawJob, JobAdmin)
admin.site.register(SearchTerm)
admin.site.register(UserRating)
admin.site.register(UserRequest)