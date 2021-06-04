from django.core.management.base import LabelCommand
from application.authentication.models import User
from django.core.exceptions import ObjectDoesNotExist


class Command(LabelCommand):
    help = 'Switch the is_active field of a superuser to True.\
            Type the email address saved for the superuser you wish to switch to active.'

    def handle_label(self, superuser_email, **options):
        """
        Change the 'is_active' field of a given superuser to True if it's not already.
        """
        try:
            superuser = User.objects.get(email=superuser_email)
            superuser.is_active = True
            superuser.save()
            return f"Le superuser ayant comme adresse email: '{superuser.email}' est désormais actif."
        except(User.DoesNotExist):
            return "L'adresse email indiquée ne correspond pas à un superuser."
