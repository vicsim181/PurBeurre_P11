from django.urls import path
from . import views

app_name = 'bookmark'

urlpatterns = [
    path('consult/', views.BookmarksView.as_view(), name='consult'),
    path('add/', views.AddBookmarkView.as_view(), name='add-bookmark'),
    # path('check/', views.CheckBookmarkView.as_view(), name='check-bookmark'),
]
