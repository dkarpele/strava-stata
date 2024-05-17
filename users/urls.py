from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('logout/', views.logout, name='logout'),
]
