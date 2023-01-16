from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class SearchTerm(models.Model):
    search_term = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.search_term}"

class KeyWord(models.Model):
    key_word = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.key_word}"

class Job(models.Model):
    company = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    job_description = models.TextField()
    job_location = models.CharField(max_length=100, null=True)
    job_site = models.CharField(max_length=50)
    job_title = models.CharField(max_length=100)
    joblisting_id = models.IntegerField(unique=True)
    language = models.CharField(max_length=50, null=True)
    first_crawling_date = models.DateField()
    last_crawling_date = models.DateField()
    key_words = models.ManyToManyField(KeyWord, blank=True)
    search_terms = models.ManyToManyField(SearchTerm, blank=True)
    joblisting_url = models.TextField(max_length=400)
    html_code = models.TextField()

    def __str__(self):
        return f"{self.job_title} at {self.company}"

class RawJob(models.Model):
    company = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=False, blank=True, null=True)
    job_description = models.TextField(blank=True, null=True)
    job_location = models.CharField(max_length=100, blank=True, null=True)
    job_site = models.CharField(max_length=50, blank=True, null=True)
    joblisting_id = models.IntegerField(null=True, unique=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=50, null=True)
    first_crawling_date = models.DateField(blank=True, null=True)
    last_crawling_date = models.DateField(blank=True, null=True)
    key_words = models.ManyToManyField(KeyWord, blank=True)
    search_terms = models.ManyToManyField(SearchTerm, blank=True)
    joblisting_url = models.TextField(max_length=400, blank=True, null=True)
    html_code = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.job_title} at {self.company}"

class UserRating(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    rating = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(10)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("job", "user")

    def __str__(self):
        return f"{self.job} (Rating: {self.rating})"

class UserRequest(models.Model):
    search_terms = models.ManyToManyField(SearchTerm, blank=True)
    key_words = models.ManyToManyField(KeyWord)
