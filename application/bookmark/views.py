from django.http.response import JsonResponse
from django.views.generic.base import View
from .models import Substitution
from application.main.models import Product
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


# Create your views here.
class BookmarksView(UpdateView):
    """
    Class holding the views of the bookmark application.
    """
    template_name = 'bookmark/bookmarks.html'
    model = Substitution

    def get(self, request):
        """
        Get function, displays the bookmarks if there are some.
        """
        current_user = request.user
        bookmarks = Substitution.get_bookmarks_by_user(current_user.id)
        data = {}
        for bookmark in bookmarks:
            data[Product.retrieve_prod_with_pk(bookmark.replacing_product_id)] = [
                 Product.retrieve_prod_with_pk(bookmark.replaced_product_id),
                 bookmark.date_creation]
        context = {'data': data}
        return render(request, self.template_name, context)

    def post(self, *args, **kwargs):
        """
        Post function, delete a bookmark when consulting them.
        """
        current_user = self.request.POST.get('user_id')
        replaced_id = self.request.POST.get('product_id')
        replacing_id = self.request.POST.get('suggestion_id')
        bookmark_to_delete = Substitution.objects.get(replaced_product_id=replaced_id,
                                                      replacing_product_id=replacing_id,
                                                      user_id=current_user)
        bookmark_to_delete.delete()
        return redirect('bookmark:consult')


class AddBookmarkView(View):
    """
    Add a bookmark
    """
    def post(self, *args):
        current_user = self.request.POST.get('user_id')
        replaced_id = self.request.POST.get('replaced_id')
        replacing_id = self.request.POST.get('replacing_id')
        Substitution.save_bookmark(replaced_id, replacing_id, current_user)
        data = {
            'status': True,
        }
        return JsonResponse(data)


# class CheckBookmarkView(View):
#     """
#     """
#     def get(self, *args):
#         replaced_id = self.request.GET.get('replaced_id')
#         replacing_id = self.request.GET.get('replacing_id')
#         user_id = self.request.GET.get('user_id')
#         print('REQUEST    :' + str(self.request))
#         print('REPLACED:   ' + str(replaced_id))
#         print('REPLACING:   ' + str(replacing_id))
#         print('USER:   ' + str(user_id))
#         try:
#             data = {
#                 'exists': Substitution.specific_bookmark(replaced_id, replacing_id, user_id),
#             }
#             if data['exists']:
#                 print('BOOKMARK FOUND')
#             else:
#                 print('BOOKMARK NOT FOUND')
#             return JsonResponse(data)
#         except (Substitution.DoesNotExist):
#             print('BOOKMARK NOT FOUND')
#             data = {}
#             return JsonResponse(data)
