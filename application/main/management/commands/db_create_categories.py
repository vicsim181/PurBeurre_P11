import json
from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from application.main.models import Category, Store


class Command(BaseCommand):
    help = 'Create the categories in the main_category table.'

    def handle(self, *args, **options):
        """
        Function handling the process of going through the list of categories.
        It then passes them as argument to create_category for the creation.
        """
        try:
            unknown = Store(name="Lieu d'achat non précisé")
            unknown.save()
        except IntegrityError:
            pass
        with open('application/main/management/commands/settings.json', 'r') as settings:
            data = json.load(settings)
        categories = data['categories']
        for main_category in categories:
            self.create_category(main_category)
            for sub_category in categories[main_category]:
                self.create_category(sub_category)

    def create_category(self, category_name):
        """
        Function creating a category in the database.
        """
        try:
            category = Category(name=category_name)
            category.save()
        except category.DoesNotExist:  # In case the value passed in category_name is empty
            raise CommandError('No category in the CATEGORIES list.')
