from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views as rest_framework_views
from . import views

urlpatterns = [
    path('create-account/', views.register, name='register'),
    path('sign-in/', auth_views.LoginView.as_view(template_name='accounts/sign-in.html'), name='sign-in'),
    path('extension-authentication/', views.extensionAuthentication, name="extension-authentication"),
    path('sign-out/', auth_views.LogoutView.as_view(template_name="accounts/sign-out.html"), name='sign-out'),
    path('api-token-auth/', rest_framework_views.obtain_auth_token, name='api-token-auth')
]