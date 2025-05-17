from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="HomeView"),
    path('login/', views.LoginView.as_view(), name='LoginView'),
    path('register/', views.RegisterView.as_view(), name='RegisterView'),
]
