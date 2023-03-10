from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, CreateView, View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from datetime import date
import time
from random import randint

from .functions.jobscout24.crawler import find_jobsites, Crawler
from .functions.utility.top_50_jobs import sort_top_50_jobs
from .functions.utility.ping_url import ping_url

from .models import Job, KeyWord, SearchTerm, RawJob, UserRating, UserRequest
from .forms import AddKeywordForm, AddSearchtermForm, UserRatingForm

# Create your views here.

class HomeView(ListView):
    model = Job
    template_name = "job_searcher/index.html"
    context_object_name = "job_list"

    def get_context_data(self, **kwargs):
        latest_crawling_date = Job.objects.latest("pk").first_crawling_date
        context = super().get_context_data(**kwargs)
        context['job_list'] = Job.objects.filter(first_crawling_date=latest_crawling_date)
        return context

""" class JobDetailView(DetailView):
    model = Job
    template_name = "job_searcher/job_detail_page.html"
    context_object_name = "job_info"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserRatingForm
        print(context)
        return context """

class JobDetailView(View):

    def get(self, request, pk):
        job = Job.objects.get(id=pk)
        return render(request, "job_searcher/job_detail_page.html", {
            "job": job,
            "form": UserRatingForm
        })

    def post(self, request, pk):
        job = Job.objects.get(id=pk)
        rating = request.POST['rating']
        user_rating = UserRating(job=job, rating=rating, user=request.user)
        try:
            user_rating.save()
        except:
            UserRating.objects.filter(job=job, user=request.user).update(rating=rating)
        return render(request, "job_searcher/job_detail_page.html", {
            "job": job,
            "form": UserRatingForm
        }) 

class NotLoggedInView(View):
    def get(self, request):
        return render(request, "job_searcher/not_logged_in_page.html")

class NotAStaffView(View):
    def get(self, request):
        return render(request, "job_searcher/not_a_staff_page.html")

class AddSearchTermsView(LoginRequiredMixin, CreateView):
    model = SearchTerm
    template_name = "job_searcher/add_keywords_or_search_terms_page.html"
    form_class = AddSearchtermForm
    success_url = "/add-search-terms/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_terms = SearchTerm.objects.all()
        context['data_points'] = search_terms
        context['kind'] = "Searchterm"
        return context

    def form_valid(self, form):
        
        if "search_term" not in self.request.POST:
            if "delete" in self.request.POST:
                id = self.request.POST["delete"]
                search_term = SearchTerm.objects.get(pk=id)
                print(search_term)
                search_term.delete()
            return redirect("/add-search-terms/")
        return super().form_valid(form)

class AddKeywordsView(LoginRequiredMixin, CreateView):
    model = KeyWord
    template_name = "job_searcher/add_keywords_or_search_terms_page.html"
    form_class = AddKeywordForm
    success_url = "/add-keywords/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        key_words = KeyWord.objects.all()
        context['data_points'] = key_words
        context['kind'] = "Keyword"
        return context

    def form_valid(self, form):
        if "key_word" not in self.request.POST:
            if "delete" in self.request.POST:
                id = self.request.POST["delete"]
                key_word = KeyWord.objects.get(pk=id)
                print(key_word)
                key_word.delete()
            return redirect("/add-keywords/")
        self.object = form.save()
        jobs_data = Job.objects.filter(job_description__contains=self.request.POST['key_word'].lower())
        key_word = KeyWord.objects.get(key_word=self.request.POST['key_word'])
        for job_data in jobs_data:
            job_data.key_words.add(key_word)
        return HttpResponseRedirect(self.get_success_url())

class PingJobsitesView(UserPassesTestMixin, View):
    def get(self, request):
        return render(request, "job_searcher/ping_jobsites_page.html")

    def post(self, request):
        jobs = Job.objects.all()
        today = date.today()
        for job in jobs:
            status_code = ping_url(job.joblisting_url)
            print(f"{status_code}: {job.joblisting_url}")
            if status_code == 200:
                job.is_active = True
                job.last_crawling_date = today
            else:
                print(f"{job.job_title} ({job.company})")
                job.is_active = False
                job.last_crawling_date = today

            try:
                job.save()
            except:
                continue

        return render(request, "job_searcher/ping_jobsites_page.html")

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('not-a-staff-page')

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
        if data["place"] != "":
            jobs = jobs.filter(job_location__contains=data["place"])
        if data["date"] != "":
            jobs = jobs.filter(first_crawling_date=data["date"])
        jobs = jobs.filter(is_active=True).distinct()
        list_jobs = jobs.values("id", "job_title", "job_location", "joblisting_url", "language", "first_crawling_date")
        list_jobs_with_scores = []
        for i in range(len(list_jobs)):
            job = jobs[i]
            job_dic = list_jobs[i]
            set_key_words = set(key_words.values_list("key_word", flat=True))
            list_job_key_words = list(job.key_words.all().values_list("key_word", flat=True))
            if data.get("search_terms"):
                set_search_terms = set(search_terms.values_list("search_term", flat=True))
                list_job_search_terms = list(job.search_terms.all().values_list("search_term", flat=True))
                job_dic['search_terms'] = list(set.intersection(set_search_terms, set(list_job_search_terms)))
            else:
                job_dic['search_terms'] = ""
            job_dic['score'] = 0
            job_dic['key_words'] = list(set.intersection(set_key_words, set(list_job_key_words)))
            for key_word in key_words:
                if key_word in job.key_words.all():
                    job_dic['score'] += 1
            
            list_jobs_with_scores.append(job_dic)

        list_top_jobs = sort_top_50_jobs(list_jobs_with_scores)

        context = self.get_context_data(form=form)
        context['jobs_list'] = list_top_jobs[:200]

        return self.render_to_response(context=context)


class ActivateCrawlerView(UserPassesTestMixin, View):
    def get(self, request):
        return render(request, "job_searcher/activate_crawler_page.html")

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


                        try:
                            job_data_saved = Job.objects.create(company=crawled_data.company_title, is_active=True, job_description=crawled_data.job_description, job_location=crawled_data.job_location,
                            job_site=dic_job_data.get("job_site"), job_title=crawled_data.job_title, joblisting_id=dic_job_data.get("joblisting_id"), first_crawling_date=today,
                            last_crawling_date=today, language = crawled_data.language, joblisting_url=dic_job_data.get("joblisting_url"), html_code=crawled_data.job_description_soup)


                            known_joblisting_ids.append(dic_job_data.get("joblisting_id"))

                        except Exception as e1:
                            if job_data_saved.joblisting_id not in known_joblisting_ids:
                                try:
                                    RawJob.objects.create(
                                    company=crawled_data.company_title, is_active=True, job_description=crawled_data.job_description, job_location=crawled_data.job_location, 
                                    job_site=dic_job_data.get("job_site"), job_title=crawled_data.job_title, joblisting_id=dic_job_data.get("joblisting_id"), first_crawling_date=today,
                                    last_crawling_date=today, language = crawled_data.language, joblisting_url=dic_job_data.get("joblisting_url"), html_code=crawled_data.job_description_soup)

                                    print("Added to RawJobs")
                                except Exception as e2:
                                    print(e2)
                            else:
                                job_data_saved = Job.objects.get(joblisting_id=job_data_saved.joblisting_id)

                        try:
                            job_data_saved.search_terms.add(search_term)

                            #Adding the matching Keywords to the new entry
                            for key_word in key_words:
                                if key_word.key_word.lower() in job_data_saved.job_description:
                                    job_data_saved.key_words.add(key_word)
                                
                            job_data_saved.save()
                        
                        except Exception as e:
                            print(e)
                                

                    else:
                        known_joblisting = Job.objects.get(joblisting_id=dic_job_data.get('joblisting_id'))
                        known_joblisting.last_crawling_date = today
                        known_joblisting.is_active = True
                        known_joblisting.search_terms.add(search_term)

                        known_joblisting.save()

                    print(f"{round(time.time() - start_time, 2)} seconds have passed.")

            return render(request, "job_searcher/activate_crawler_page.html")

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('not-a-staff-page')