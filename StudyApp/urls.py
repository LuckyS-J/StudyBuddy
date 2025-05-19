from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="HomeView"),
    path('login/', views.MyLoginView.as_view(), name='LoginView'),
    path('register/', views.RegisterView.as_view(), name='RegisterView'),
    path('logout/', views.MyLogoutView.as_view(), name='LogoutView'),
    path('test/', views.TestView.as_view(), name='TestView'),
    path('add/', views.AddGoalView.as_view(), name='AddView'),
    path('delete/<int:id>/', views.DeleteView.as_view(), name='DeleteView'),
]
