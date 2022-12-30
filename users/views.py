from django.shortcuts import render, redirect
from django.views.generic import View, CreateView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.messages import constants as messages

# Create your views here.

class ProfileView(View):
    def get(self, request):
        return render(request, "job_searcher/index.html")

class SuccessfulRegisterView(View):
    def get(self, request):
        return render(request, "registration/successful_register.html")

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
