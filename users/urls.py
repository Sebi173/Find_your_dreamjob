from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("logout/", views.LogoutView.as_view(), name="logout-page"),
    path("", include('django.contrib.auth.urls')),
    path("register/", views.RegisterView.as_view(), name="register-page"),
    path("profile/", views.ProfileView.as_view(), name="profile-page"),
    path("register/success/", views.SuccessfulRegisterView.as_view(), name="register-success-page"),
]