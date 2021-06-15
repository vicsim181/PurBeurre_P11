from application.bookmark.views import User
from django.http.response import HttpResponse
from pur_beurre.settings.base import EMAIL_HOST_USER
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ObjectDoesNotExist
from .forms import RegisterForm


class RegisterView(FormView):
    """
    View managing the registration of a user.
    """
    template_name = 'authentication/register.html'  # comme un get() integré
    form_class = RegisterForm  # notre formulaire
    success_url = 'confirmation'  # url de notre page de success
    activation_token = PasswordResetTokenGenerator()

    def form_valid(self, form: form_class):
        """
        Function called when the form is filled up and the button clicked.
        It only comes if the data in the form are valid.
        """
        form.save()
        new_user_email = form['email'].value()
        link = RegisterView.generating_link(self, new_user_email)
        RegisterView.sending_email(self, link, new_user_email)
        return super().form_valid(form)

    def generating_link(self, email):
        """
        Function called during the process of validating the form.
        It's going to use the email address given by the user in the form and prepare the link in the email. 
        """
        new_user = User.objects.get(email=email)
        generated_token = self.activation_token.make_token(new_user)
        new_user.registration_token = generated_token
        new_user.save()
        encoded_token = urlsafe_base64_encode(force_bytes(generated_token))
        current_domain = self.request.get_host()
        current_url = self.request.get_full_path()
        link = 'http://' + str(current_domain + current_url) + 'validation/'\
               + urlsafe_base64_encode(force_bytes(email)) + '/' + encoded_token
        return link

    def sending_email(self, link, email):
        """
        Function called once the link is generated.
        It sends the activation email to the new user.
        """
        send_mail(
            "Lien d'activation de votre compte PurBeurre.",
            "Cliquez sur le lien d'activation pour valider votre compte: \n" + link + ".\n\nL'équipe PurBeurre.",
            EMAIL_HOST_USER,
            [email],
            fail_silently=False)


class ConfirmationView(TemplateView):
    template_name = 'authentication/confirmation.html'


class ValidationView(FormView):
    """
    View managing the step when the user has to confirm his registration through his emails.
    """
    template_name = 'authentication/confirmation.html'  # template de validation de l'enregistrement.
    success_url = 'success'

    def get(self, request, uid, utoken):
        try:
            email_to_find = force_text(urlsafe_base64_decode(uid))
            token_to_find = force_text(urlsafe_base64_decode(utoken))
            user = User.objects.get(email=email_to_find, registration_token=token_to_find)
            user.is_active = True
            user.save()
            return redirect('authentication:success')
        except(User.DoesNotExist, TypeError, ValueError):
            return render(request, template_name='page_not_found.html')


class SuccessView(TemplateView):
    """
    Template displayed when registered.
    """
    template_name = 'authentication/registered.html'


class ConsultAccountView(TemplateView):
    """
    View called when consulting the user account.
    """
    template_name = 'authentication/account.html'

    def get(self, request):
        return render(request, self.template_name, locals())
