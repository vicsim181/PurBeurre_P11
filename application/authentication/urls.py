from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authentication/logout.html'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('account/', views.ConsultAccountView.as_view(), name='account'),
    path('register/success', views.SuccessView.as_view(), name='success'),  # url de la page de success
]
