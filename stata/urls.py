from django.urls import path

from . import views

app_name = "stata"

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('activities/', views.Activities.as_view(), name='activities'),
]