from django.shortcuts import render, redirect
from django.views import View
from .models import Goals, Users
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.

class HomeView(View):

  def get(self, request):
    goals = Goals.objects.all()
    return render(request, 'StudyApp/index.html', {
      'goals':goals
    })
  

class RegisterView(View):
  
  def get(self, request):
    return render(request, 'StudyApp/register.html')

  def post(self, request):
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        username = request.POST.get('username').strip()

        if not username or not password:
            messages.error(request, "All fields are required!.")
            return render(request, 'StudyApp/register.html')
        
        if Users.objects.filter(username=username).exists():
            messages.error(request, "User with that email already exist!.")
            return render(request, self.template_name)
        
        user = Users(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created. You can login.")
        return redirect(reverse('LoginView'))

class LoginView(View):
  def get(self, request):
    return render(request, 'StudyApp/login.html')
  
  def post(self, request):
    email = request.POST['email']
    password = request.POST['password']
    return redirect(reverse('HomeView'))