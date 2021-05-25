from django.urls import path
from . import views

app_name = 'bookmark'

urlpatterns = [
    path('consult/', views.BookmarksView.as_view(), name='consult'),
]
