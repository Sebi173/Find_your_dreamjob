from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home-page"),
    path("add-search-terms/", views.AddSearchTermsView.as_view(), name="add-search-terms-page"),
    path("add-keywords/", views.AddKeywordsView.as_view(), name="add-keywords-page"),
    path("activate-crawler/", views.ActivateCrawlerView.as_view(), name="activate-crawler-page"),
    path("ping-jobsites/", views.PingJobsitesView.as_view(), name="ping-jobsites-page"),
    path("keyword-engine/", views.KeywordEngineView.as_view(), name="keyword-engine-page"),
    path("not-logged-in/", views.NotLoggedInView.as_view(), name="not-logged-in-page"),
    path("not-a-staff/", views.NotAStaffView.as_view(), name="not-a-staff-page"),
    path("<int:pk>", views.JobDetailView.as_view(), name="job-detail-page"),
]

