from django.shortcuts import render
from django.views import View
from .models import Goal
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.views.generic.edit import FormView
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class HomeView(View):

  def get(self, request):
    goals = Goal.objects.all()
    return render(request, 'StudyApp/index.html', {
      'goals':goals
    })
  
class RegisterView(FormView):
    template_name = 'StudyApp/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('LoginView')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
  

class MyLoginView(LoginView):
    template_name = 'StudyApp/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('HomeView')

    def get_success_url(self):
        return self.success_url


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('HomeView')


class TestView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        goals = Goal.objects.all()
        return render(request, 'StudyApp/index.html', {'goals': goals})