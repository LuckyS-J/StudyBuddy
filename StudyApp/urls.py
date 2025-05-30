from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.HomeView.as_view(), name="HomeView"),
    path('login/', views.MyLoginView.as_view(), name='LoginView'),
    path('register/', views.RegisterView.as_view(), name='RegisterView'),
    path('logout/', views.MyLogoutView.as_view(), name='LogoutView'),
    path('test/', views.TestView.as_view(), name='TestView'),
    path('add/', views.AddGoalView.as_view(), name='AddView'),
    path('delete/<int:id>/', views.DeleteView.as_view(), name='DeleteView'),
    path('details/<int:id>/', views.MyDetailView.as_view(), name='DetailView'),
    path('task/<int:task_id>/toggle/',
         views.toggle_task_done, name='toggle_task_done'),
    path('task/delete/<int:id>/', views.delete_task, name='DeleteTask'),
    path('note/delete/<int:id>/', views.delete_note, name='DeleteNote'),
    path('goal/change-status/<int:id>/',
         views.change_goal_status, name='ChangeGoalStatus'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
