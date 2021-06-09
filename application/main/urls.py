from django.urls.conf import path, re_path
from .views import HomeView, ProductView, ResultsView, MentionsView, CategoriesView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('mentionslegales/', MentionsView.as_view(), name='mentions'),
    # path('list/', ProductListView.as_view(), name='product-list'),
    path('results/', ResultsView.as_view(), name='results'),
    path('product/<int:pk>', ProductView.as_view(), name='product_detail'),
    path('categories/', CategoriesView.as_view(), name='categories'),
]
