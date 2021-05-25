import json
from django.core.management.base import LabelCommand, CommandError
from application.main.models import Category, Product, Store


class Command(LabelCommand):
    help = 'Delete a category from the database.'      

    def handle_label(self, category, **options):
        """
        Function checking if the category is a main or sub category.
        Depending on it, it will directly delete all the appropriate products related to it.

        """
        self.category = category.lower()
        with open('application/main/management/commands/settings.json', 'r') as settings:
            data = json.load(settings)
        self.categories = data['categories']
        self.categ_type = None
        if self.category in self.categories:
            self.stdout.write(self.category + ' is a Main category.')
            self.categ_type = 'main'
        else:
            for main in self.categories:
                if self.category in self.categories[main]:
                    self.stdout.write(self.category + ' is a Sub category.')
                    self.categ_type = 'sub'
        if self.categ_type is None:
            self.stdout.write("Cette catégorie n'existe pas.")
        else:
            cat_id = Category.objects.get(name=self.category)
            self.get_and_delete_products(cat_id)
            self.get_and_delete_categories()
        return

    def get_and_delete_products(self, cat_id):
        """
        Function gathering the products from the selected category.
        """
        Product.objects.filter(category=cat_id).delete()
        self.stdout.write("All the products from the category " + self.category + " have been deleted")
        return

    def get_and_delete_categories(self):
        """
        Function gathering the main and/or sub categories and delete them from the database.
        """
        if self.categ_type == 'main':
            for sub_cat in self.categories[self.category]:
                Category.objects.get(name=sub_cat).delete()
                self.stdout.write("Category: " + sub_cat + " deleted.")
            Category.objects.get(name=self.category).delete()
            self.stdout.write("Category: " + self.category + " deleted.")
        elif self.categ_type == 'sub':
            Category.objects.get(name=self.category).delete()
            self.stdout.write("Category: " + self.category + " deleted.")
        else:
            self.stdout.write('Erreur dans la valeur de self.cat_type. Catégorie ni main ni sub.')    
        return
