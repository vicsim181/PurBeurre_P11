import json
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django import forms
from .models import Product
from application.bookmark.models import Substitution


# Create your views here.
class HomeView(FormView):
    """
    View displaying the homepage of the website.
    """
    template_name = 'main/index.html'
    form_class = forms.Form


# class ProductListView(View):
#     """
#     """
#     def get(self, *args):
#         user_input = self.request.GET.get('recherche')
#         products = Product.retrieve_product_bis(user_input)
#         data = {
#             'products': {}
#         }
#         for product in products:
#             result = Product.retrieve_prod_with_code(products[product])
#             data['products'][product] = result.name
#         return JsonResponse(data)


class ResultsView(TemplateView):
    """
    View displaying the results of a user request.
    """
    template_name = 'main/results.html'

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        current_user = self.request.user
        user_input = self.request.GET.get('recherche')
        product, category = Product.retrieve_product(user_input)
        if product:
            suggestions = Product.generate_suggestions(category, product)
            user_favs = Substitution.check_favs(product, current_user)
        else:
            suggestions = None
            user_favs = []
        context['user_favs'] = user_favs
        context['product'] = product
        context['suggestions'] = suggestions
        context['category'] = category
        return context


class ProductView(DetailView):
    """
    View displaying the detail page of a product.
    """
    template_name = 'main/product_detail.html'
    model = Product

    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        stores = product.store.all()
        product_stores = [store.name for store in stores]
        return render(request, self.template_name, locals())


class MentionsView(TemplateView):
    """
    View displaying the mentions légales page.
    """
    template_name = 'mentions.html'


class CategoriesView(TemplateView):
    """
    View displaying the categories list page.
    """
    template_name = 'main/categories.html'

    def get(self, request):
        with open('application/main/management/commands/settings.json', 'r') as settings:
            data = json.load(settings)
        categories = data['categories']
        return render(request, self.template_name, locals())
