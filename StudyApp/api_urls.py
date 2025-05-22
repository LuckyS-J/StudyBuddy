from django.urls import path
from . import api_views

urlpatterns = [
    path('get-all/', api_views.getData),
    path('get/<int:id>', api_views.getData),
]
