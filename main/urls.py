from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('activities/site/', views.site_activity, name="page-visits")
]