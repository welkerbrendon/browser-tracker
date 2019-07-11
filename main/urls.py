from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('activities/site/', views.site_activity, name="page-visits"),
    path('site-visits/', views.view_site_visits, name="site-visits")
]