from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from application.main.models import Product


# Create your models here.
class Substitution(models.Model):
    """
    Model class for the substitution, linked with the bookmark application.
    """
    target_product = models.ForeignKey(Product, related_name="target_product", on_delete=CASCADE)
    source_product = models.ForeignKey(Product, related_name="source_product", on_delete=CASCADE)
    date_creation = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(get_user_model(), on_delete=CASCADE)

    class Meta:
        """
        Meta class adding a constraint on three of the four elements of the model
        (target_product, source_product and user).
        """
        db_table = 'bookmark_substitution'
        constraints = [
            models.UniqueConstraint(fields=['target_product', 'source_product', 'user_id'],
                                    name='unique_substitution_user')
        ]

    def get_bookmarks_by_user(user_id):
        """
        Get all the bookmarks for a specific user if it has some.
        """
        bookmarks = Substitution.objects.filter(user_id=user_id)
        return bookmarks

    def save_bookmark(source_id, target_id, user_id):
        """
        Save a bookmark with the three parameters required.
        """
        bookmark_to_save = Substitution(source_product_id=source_id, target_product_id=target_id, user_id=user_id)
        bookmark_to_save.save()

    def specific_bookmark(source_id, target_id, user_id):
        """
        Get a specific bookmark if it exists.
        """
        try:
            substitution = Substitution.objects.get(source_product_id=source_id, target_product_id=target_id, user_id=user_id)
            if substitution:
                return True
        except ObjectDoesNotExist:
            return False

    def check_favs(product, current_user):
        """
        Checks the bookmarks of a user with a particular source_product.
        Allow to display or not the option to add a bookmark in the results page.
        """
        user_favs = [Product.objects.get(pk=subst.target_product_id).id
                     for subst in
                     Substitution.objects.filter(source_product_id=product.id, user_id=current_user.id).all()]
        return user_favs
