from collections import namedtuple
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authentication/logout.html'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('account/', views.ConsultAccountView.as_view(), name='account'),
    path('register/confirmation', views.ConfirmationView.as_view(), name='confirmation'),  # url de la page d'attente de confirmation du client
    path('register/validation/<str:uid>/<str:utoken>', views.ValidationView.as_view(), name='validation'), # url de la page de validation
    path('register/success', views.SuccessView.as_view(), name='success'),  # url de la page de success
    path('account/change-password', auth_views.PasswordChangeView.as_view(template_name='authentication/change-password.html', success_url='password-changed'), name='change-password'),
    path('account/password-changed', views.PasswordChanged.as_view(), name='password-changed'),
]
