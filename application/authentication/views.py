from application.bookmark.views import User
from django.http.response import HttpResponse
from pur_beurre.settings.base import EMAIL_HOST_USER
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .forms import RegisterForm
from .token import activation_token


class RegisterView(FormView):
    """
    View managing the registration of a user.
    """
    template_name = 'authentication/register.html'  # comme un get() integré
    form_class = RegisterForm  # notre formulaire
    success_url = 'confirmation' # url de notre page de success

    def form_valid(self, form: form_class):
        new_user_email = form['email'].value()
        form.save()
        new_user = User.objects.get(email=new_user_email)
        generated_token = activation_token.make_token(new_user)
        new_user.registration_token = generated_token
        encoded_token = urlsafe_base64_encode(force_bytes(generated_token))
        new_user.save()
        current_domain = self.request.get_host()
        current_url = self.request.get_full_path()
        link = 'http://' + str(current_domain + current_url) + 'validation/'\
               + urlsafe_base64_encode(force_bytes(new_user_email)) + '/' + encoded_token
        send_mail(
            "essai",
            "Lien d'activation " + link + ".",
            EMAIL_HOST_USER,
            [new_user_email],
            fail_silently=False)
        return super().form_valid(form)


class ConfirmationView(TemplateView):
    template_name = 'authentication/confirmation.html'


class ValidationView(FormView):
    """
    View managing the step when the user has to confirm his registration through his emails.
    """
    template_name = 'authentication/confirmation.html' # template de validation de l'enregistrement.
    success_url = 'success'

    def get(self, request, uid, utoken):
        email_to_find = force_text(urlsafe_base64_decode(uid))
        token_to_find = force_text(urlsafe_base64_decode(utoken))
        print('EMAIL FOUND: ' + email_to_find)
        print('TOKEN FOUND: ' + token_to_find)
        try:
            user = User.objects.get(email=email_to_find, registration_token=token_to_find)
            if user:
                user.is_active = True
                user.save()
                return redirect('authentication:success')
            else:
                return HttpResponse('Trouve pas user')
        except(User.DoesNotExist, TypeError, ValueError):
            return HttpResponse('Inscription échouée')
    

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


class PasswordChanged(TemplateView):
    """
    """
    template_name = 'authentication/password-changed.html'
