from django.shortcuts import render
from django.views import View
from .models import Goals

# Create your views here.

class HomeView(View):

  def get(self, request):
    goals = Goals.objects.all()
    return render(request, 'StudyApp/index.html', {
      'goals':goals
    })