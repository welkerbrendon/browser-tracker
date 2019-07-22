from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('activities/site/', views.site_activity, name="page-visits"),
    path('site-visits/', views.view_site_visits, name="site-visits"),
    path('data-summary/raw-data', views.site_visit_raw_data, name="raw-summary"),
    path('data-summary/', views.data_summary, name="data-summary")
]