from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Goal
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm, AddGoalForm
from django.views.generic.edit import FormView
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden

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
    form_class = LoginForm
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


class AddGoalView(LoginRequiredMixin, FormView):

    login_url = '/login/'
    redirect_field_name = 'next'
    
    template_name = 'StudyApp/add.html'
    form_class = AddGoalForm
    success_url = reverse_lazy('HomeView')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)
    

class DeleteView(LoginRequiredMixin, View):
    def post(self, request, id):
        goal = get_object_or_404(Goal, id=id)

        if goal.user != request.user:
            return HttpResponseForbidden("You do not have permission to delete this goal.")

        goal.delete()
        return redirect('HomeView')
        