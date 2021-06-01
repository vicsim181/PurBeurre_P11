from collections import namedtuple
from django.conf.urls import url
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views, forms

app_name = 'authentication'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html',
                                                authentication_form=forms.CustomAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authentication/logout.html'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('account/', views.ConsultAccountView.as_view(), name='account'),
    path('register/confirmation', views.ConfirmationView.as_view(), name='confirmation'),
    path('register/validation/<str:uid>/<str:utoken>', views.ValidationView.as_view(), name='validation'),
    path('register/success', views.SuccessView.as_view(), name='success'),
    path('account/change-password', auth_views.PasswordChangeView.as_view(template_name='authentication/change-password.html',
                                                                          success_url='password-changed'), name='change-password'),
    path('account/password-changed', auth_views.PasswordChangeDoneView.as_view(template_name='authentication/password-changed.html'), name='password-changed'),
    path('login/reset', auth_views.PasswordResetView.as_view(template_name='authentication/password_reset_1.html',
                                                             email_template_name='authentication/password_reset_email.html',
                                                             subject_template_name='authentication/password_reset_subject.txt',
                                                             success_url='reset_confirmed'),
                                                             name='forgotten-password'),
    path('login/reset_confirmed', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_2.html'), name='reset_confirmed'),
    path('login/reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_3.html',
                                                                                     success_url=reverse_lazy('authentication:password_reset_complete')),
                                                                                     name='password_reset_confirm'),
    path('login/reset/confirmed', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_4.html'), name='password_reset_complete'),
]
