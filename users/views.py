from django.shortcuts import render, redirect
from django.views.generic import View, CreateView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout

# Create your views here.

class ProfileView(View):
    def get(self, request):
        return render(request, "job_searcher/index.html")

class SuccessfulRegisterView(View):
    def get(self, request):
        return render(request, "registration/successful_register.html")

class LogoutView(View):
    def get(self, request):
        return render(request, "registration/logout.html")
    def post(self, request):
        if "logout" in request.POST:
            logout(request)
            return render(request, "registration/logout.html")
        elif "login" in request.POST:
            return redirect("/user/login")
        elif "register" in request.POST:
            return redirect("/user/register")
        return render(request, "registration/logout.html")

class RegisterView(CreateView):
    model = User
    fields = ["email", "username", "password"]
    template_name = "registration/register.html"
    success_url = "success/"

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        choosen_password = cleaned_data['password']
        confirmed_password = self.request.POST['confirmed_password']
        if confirmed_password == choosen_password:
            new_user = form.save()
            login(self.request, new_user)
            return redirect("success/")
        else:
            return redirect('/user/register/')
