from django.http.response import HttpResponseRedirect
from application.main.models import Product
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.urls import reverse
from .models import Substitution

User = get_user_model()


# Create your views here.
class BookmarksView(TemplateView):
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
            data[Product.retrieve_prod_with_pk(bookmark.target_product_id)] = [
                 Product.retrieve_prod_with_pk(bookmark.source_product_id),
                 bookmark.date_creation]
        context = {'data': data}
        return render(request, self.template_name, context)

    def post(self, *args, **kwargs):
        """
        Post function, add or delete a bookmark depending on the user request.
        """
        aim = self.request.POST.get('aim')
        current_user = self.request.user
        source_id = self.request.POST.get('product_id')
        target_id = self.request.POST.get('suggestion_id')
        recherche = self.request.POST.get('recherche')
        next = self.request.POST.get('next', '/')
        retour = f'{next}?recherche={recherche}'
        # if aim == 'add':
        #     Substitution.save_bookmark(source_id, target_id, current_user.id)
        #     # return redirect(retour)
        if aim == 'delete':
            bookmark_to_delete = Substitution.objects.get(source_product_id=source_id,
                                                          target_product_id=target_id,
                                                          user_id=current_user.id)
            bookmark_to_delete.delete()
            return redirect('bookmark:consult')
        else:
            return


class AddBookmarkView(View):

    """
    View used to add bookmark.
    """
    def post(self, *args):
        """
        Function used when a product is added to the bookmarks.
        Calls the appropriate function of the Substitution model.
        """
        current_user = self.request.user
        source_id = self.request.POST.get('product_id')
        target_id = self.request.POST.get('suggestion_id')
        recherche = self.request.POST.get('recherche')
        print('RECHERCHE:  ' + str(recherche))
        try:
            Substitution.save_bookmark(source_id, target_id, current_user.id)
            return HttpResponseRedirect(reverse('results', args=(recherche)))
        except(Substitution.DoesNotExist):
            return HttpResponse(reverse('main:results', args=(recherche)))

#  source_id=product.id target_id=suggestion.id %}
# request, source_id, target_id
# <int:source_id>/<int:target_id>
