from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, View
from django.db import IntegrityError
from django.http import HttpResponseRedirect

from datetime import date
import time
from random import randint

from .functions.jobscout24.crawler import find_jobsites, Crawler
from .functions.utility.top_50_jobs import sort_top_50_jobs

from .models import Job, KeyWord, SearchTerm, RawJob, UserRating, UserRequest

# Create your views here.

class HomeView(ListView):
    model = Job
    template_name = "job_searcher/index.html"
    context_object_name = "job_list"

class JobDetailView(DetailView):
    model = Job
    template_name = "job_searcher/job_detail_page.html"
    context_object_name = "job_info"

class AddSearchTermsView(CreateView):
    model = SearchTerm
    template_name = "job_searcher/add_keywords_or_search_terms_page.html"
    fields = "__all__"
    success_url = "add-search-terms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_terms = SearchTerm.objects.all()
        context['data_points'] = search_terms
        context['kind'] = "Searchterm"
        return context

class AddKeywordsView(CreateView):
    model = KeyWord
    template_name = "job_searcher/add_keywords_or_search_terms_page.html"
    fields = "__all__"
    success_url = "add-keywords"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        key_words = KeyWord.objects.all()
        context['data_points'] = key_words
        context['kind'] = "Keyword"
        return context


    def form_valid(self, form):
        self.object = form.save()
        jobs_data = Job.objects.filter(job_description__contains=self.request.POST['key_word'].lower())
        key_word = KeyWord.objects.get(key_word=self.request.POST['key_word'])
        for job_data in jobs_data:
            job_data.key_words.add(key_word)
        return HttpResponseRedirect(self.get_success_url())

class KeywordEngineView(CreateView):
    model = UserRequest
    template_name = "job_searcher/keyword_engine_page.html"
    fields = "__all__"

    def form_valid(self, form):
        data = self.request.POST
        key_words = KeyWord.objects.filter(pk__in=data.getlist('key_words'))
        if data.get("search_terms"):
            search_terms = SearchTerm.objects.filter(pk__in=data.getlist('search_terms'))
            jobs = Job.objects.filter(search_terms__in=search_terms)
            jobs = jobs.filter(key_words__in=key_words)
        else:
            jobs = Job.objects.filter(key_words__in=key_words)
        jobs = jobs.filter(is_active=True).distinct()
        list_jobs = jobs.values("id", "job_title", "job_location", "joblisting_url", "language", "first_crawling_date")
        list_jobs_with_scores = []
        for i in range(len(list_jobs)):
            job = jobs[i]
            job_dic = list_jobs[i]
            set_key_words = set(key_words.values_list("key_word", flat=True))
            list_job_key_words = list(job.key_words.all().values_list("key_word", flat=True))
            set_search_terms = set(search_terms.values_list("search_term", flat=True))
            list_job_search_terms = list(job.search_terms.all().values_list("search_term", flat=True))
            job_dic['score'] = 0
            job_dic['key_words'] = list(set.intersection(set_key_words, set(list_job_key_words)))
            job_dic['search_terms'] = list(set.intersection(set_search_terms, set(list_job_search_terms)))
            for key_word in key_words:
                if key_word in job.key_words.all():
                    job_dic['score'] += 1
            
            list_jobs_with_scores.append(job_dic)

        list_top_50_jobs = sort_top_50_jobs(list_jobs_with_scores)

        context = self.get_context_data(form=form)
        context['jobs_list'] = list_top_50_jobs

        return self.render_to_response(context=context)


class ActivateCrawlerView(View):
    def get(self, request):
        return render(request, "job_searcher/activate-crawler-page.html")

    def post(self, request):
        if 'activate_crawler' in request.POST:

            number_of_pages_per_search_term = 5

            key_words = KeyWord.objects.all()
            today = date.today()
            known_joblisting_ids = list(Job.objects.values_list('joblisting_id', flat=True))

            #Start crawling for all the Search Terms
            search_terms = SearchTerm.objects.all()

            for search_term in search_terms:
                print(search_term)
                list_jobs_data = find_jobsites(number_of_pages_per_search_term, search_term.search_term)

                for dic_job_data in list_jobs_data:
                    
                    start_time = time.time()

                    if int(dic_job_data.get('joblisting_id')) not in known_joblisting_ids:
                        time.sleep(randint(0,3))
                        crawled_data = Crawler(dic_job_data.get("joblisting_url"))

                        job_data = Job(company=crawled_data.company_title, is_active=True, job_description=crawled_data.job_description, job_location=crawled_data.job_location,
                            job_site=dic_job_data.get("job_site"), job_title=crawled_data.job_title, joblisting_id=dic_job_data.get("joblisting_id"), first_crawling_date=today,
                            last_crawling_date=today, language = crawled_data.language, joblisting_url=dic_job_data.get("joblisting_url"), html_code=crawled_data.job_description_soup)

                        raw_job_data = RawJob(
                                company=crawled_data.company_title, is_active=True, job_description=crawled_data.job_description, job_location=crawled_data.job_location, 
                                job_site=dic_job_data.get("job_site"), job_title=crawled_data.job_title, joblisting_id=dic_job_data.get("joblisting_id"), first_crawling_date=today,
                                last_crawling_date=today, language = crawled_data.language, joblisting_url=dic_job_data.get("joblisting_url"), html_code=crawled_data.job_description_soup)

                        try:
                            job_data.save()
                            known_joblisting_ids.append(dic_job_data.get("joblisting_url"))

                        except IntegrityError:
                            print("IntegrityError")

                            if job_data.joblisting_id not in known_joblisting_ids:
                                print("Added to RawJobs")
                                try:
                                    raw_job_data.save()
                                except IntegrityError:
                                    pass

                        except:
                            print('Crawl failed')
                            try:
                                raw_job_data.save()
                            except IntegrityError:
                                pass


                        #Waiting until the database has saved our new entry
                        was_received_by_db = False

                        while was_received_by_db == False:
                            time.sleep(0.05)
                            if int(job_data.joblisting_id) in Job.objects.values_list("joblisting_id", flat=True):
                                job_data = Job.objects.get(joblisting_id=job_data.joblisting_id)
                                job_data.search_terms.add(search_term)
                                was_received_by_db = True

                        #Adding the matching Keywords to the new entry
                        for key_word in key_words:
                            if key_word.key_word.lower() in job_data.job_description:
                                job_data.key_words.add(key_word)
                                

                    else:
                        known_joblisting = Job.objects.get(joblisting_id=dic_job_data.get('joblisting_id'))
                        known_joblisting.last_crawling_date = today
                        known_joblisting.is_active = True
                        known_joblisting.search_terms.add(search_term)

                        known_joblisting.save()

                    print(f"{round(time.time() - start_time, 2)} seconds have passed.")

            return render(request, "job_searcher/activate-crawler-page.html")
