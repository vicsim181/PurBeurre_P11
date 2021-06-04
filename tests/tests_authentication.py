from os import link
from django.contrib.auth.forms import UsernameField
# import time
from django.http import request, response
from django.test import TestCase, RequestFactory
from application.authentication.models import User
from application.authentication.views import RegisterView, ConsultAccountView, ValidationView
from application.authentication.forms import RegisterForm
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from unittest.mock import patch
from selenium import webdriver


firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = False


# Create your tests here.
class RegisterTest(TestCase):
    """
    Test functions of the registration functionality.
    """
    def setUp(self):
        self.user_test = User(email='essai@gmail.com', password=None, first_name='essai', last_name='REGISTER')
        self.user_test.set_password('sUp€rP@ssw0rd')
        self.user_test.save()

    def test_user_created(self):
        print("\nTEST - User --> Register\n")
        user_test = User.objects.get(email='essai@gmail.com')
        print("self.assertEqual(user_test.first_name, 'essai')")
        self.assertEqual(user_test.first_name, 'essai')
        print("Assert Done")

    def test_str_(self):
        print("\nTEST - User --> __str__()\n")
        print("self.assertEqual(self.user_test, 'essai REGISTER essai@gmail.com')")
        self.assertEqual(str(self.user_test), 'essai REGISTER essai@gmail.com')
        print("Assert Done")

    def test_get_full_name(self):
        print("\nTEST - User --> get_full_name()\n")
        print("self.assertEqual(self.user_test.get_full_name(), 'essai REGISTER')")
        self.assertEqual(self.user_test.get_full_name(), 'essai REGISTER')
        print("Assert Done")

    def test_get_email(self):
        print("\nTEST - User --> get_email()\n")
        print("self.assertEqual(user_test.get_email(), 'essai@gmail.com')")
        self.assertEqual(self.user_test.get_email(), 'essai@gmail.com')
        print("Assert Done")

    def test_has_perm(self):
        print("\nTEST - User --> has_perm()\n")
        print("self.assertTrue(self.test_user.has_perm('view_product'))")
        self.assertTrue(self.user_test.has_perm('view_product'))
        print('ASSERT DONE')


class TestRegisterView(TestCase):
    """
    Test class for RegisterView.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.activation_token = PasswordResetTokenGenerator()
        self.data = {'email': 'essai@email.fr',
                     'first_name': 'essai',
                     'last_name': 'TEST',
                     'password1': 'sup€rP@ssw0rd',
                     'password2': 'sup€rP@ssw0rd'
                    }
        self.request = self.factory.post('register/', data=self.data)

    def test_registerview_get(self):
        print("\nTEST - REGISTERVIEW --> def get()\n")
        request = self.factory.get('register/', )
        response = RegisterView.as_view()(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print('Assert Done')

    def test_registerview_generating_link(self):
        """
        Unitary test of the function generating_link() in the RegisterView.
        Once the user filled the form and data is validated and email will be sent with a link.
        We check that the link is well generated.
        """
        print("\nTEST - REGISTERVIEW --> def generating_link()\n")
        email_test = 'essai@email.fr'
        User.objects.create_user(username='test',
                                 email=email_test,
                                 first_name='essai',
                                 last_name='TEST',
                                 password='mysup€rP@ssw0rd')
        link_test = RegisterView.generating_link(self, email_test)
        print("\nself.assertIn('http://testserver/registervalidation/', link_test)")
        self.assertIn('http://testserver/registervalidation/', link_test)
        print("ASSERT 1 DONE")

    def test_registerview_sending_email(self):
        """
        Unitary test of the function sending-email() in the RegisterView.
        Once the user filled the form and data is validated and email will be sent with a link.
        We check that the email is correctly sent.
        """
        print("\nTEST - REGISTERVIEW --> def sending_email()\n")
        link_test = "Ceci est un lien d'essai."
        email_test = 'essai@email.fr'
        RegisterView.sending_email(self, link_test, email_test)
        print("\nself.assertEqual(len(mail.outbox), 1)")
        self.assertEqual(len(mail.outbox), 1)
        print("ASSERT 1 DONE")
        print("\nself.assertEqual(mail.outbox[0].subject, \"Lien d'activation de votre compte PurBeurre.\")")
        self.assertEqual(mail.outbox[0].subject, "Lien d'activation de votre compte PurBeurre.")
        print("ASSERT 2 DONE")

    def test_registerview_post(self):
        """
        Integration test of the RegisterView.
        Once the user filled the form and data is validated and email will be sent with a link.
        We check the whole process, step by step like in the previous unitary tests.
        """
        response = RegisterView.as_view()(self.request)
        print("\nself.assertEqual(response.status_code, 302)")
        self.assertEqual(response.status_code, 302)
        print("ASSERT 1 DONE")
        print("\nUser.objects.get(email=essai@email.fr) is True")
        new_user = User.objects.get(email=self.data['email'])
        self.assertTrue(new_user)
        print("ASSERT 2 DONE")
        print("\nself.assertEqual(len(mail.outbox), 1)")
        self.assertEqual(len(mail.outbox), 1)
        print("ASSERT 3 DONE")
        print("\nself.assertEqual(mail.outbox[0].subject, \"Lien d'activation de votre compte PurBeurre.\")")
        self.assertEqual(mail.outbox[0].subject, "Lien d'activation de votre compte PurBeurre.")
        print("ASSERT 4 DONE")
        print("\nself.assertIn('http://testserver/registervalidation/', link sent by email)")
        self.assertIn('http://testserver/registervalidation/', mail.outbox[0].body)
        print("ASSERT 5 DONE")


class TestConsultAccountView(TestCase):
    """
    Test class for ConsultAccountView.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.test_user = User.objects.create_user(username='test',
                                                  email='essai123@gmail.fr',
                                                  password='lol175+essai')

    def test_consultaccountview_get(self):
        print("\nTEST - CONSULTACCOUNTVIEW --> def get()\n")
        request = self.factory.get('account/', )
        request.test_user = self.test_user
        response = ConsultAccountView.as_view()(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print('Assert Done')


class TestValidationView(TestCase):
    """
    Test class for ValidationView
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.test_token = 'ceciestunessaidetoken123456'
        self.test_email = 'essai@email.fr'
        self.test_user = User.objects.create_user(username='test',
                                                  email=self.test_email,
                                                  first_name='essai',
                                                  last_name='TEST',
                                                  password='mysup€rP@ssw0rd',
                                                  registration_token=self.test_token,
                                                  is_active=False)

    def test_validationview_get_right_data(self):
        """
        Unitary test for the function get().
        Test the ability to find a new user with the correct link in the activation email.
        We check the function redirect to the url '/user/register/success'.
        """
        print("\nTEST - VALIDATIONVIEW --> def get_right_data()\n")
        test_uid = urlsafe_base64_encode(force_bytes(self.test_email))
        test_utoken = urlsafe_base64_encode(force_bytes(self.test_token))
        test_request = self.factory.get('register/validation/')
        response = ValidationView.as_view()(test_request, test_uid, test_utoken)
        print("self.assertEqual(response.status_code, 302)")
        self.assertEqual(response.status_code, 302)
        print("ASSERT 1 DONE")
        print("self.assertEqual('/user/register/success', response.url)")
        self.assertEqual("/user/register/success", response.url)
        print("ASSERT 2 DONE")

    def test_validationview_get_wrong_data(self):
        """
        Unitary test for the function get().
        Test the ability to return an error message when the data passed in the url is not corresponding to a real user.
        """
        print("\nTEST - VALIDATIONVIEW --> def get_wrong_data()\n")
        test_wrong_email = "mauvais@email.fr"
        test_wrong_token = "ceciestunmauvaistoken654321"
        test_uid = urlsafe_base64_encode(force_bytes(test_wrong_email))
        test_utoken = urlsafe_base64_encode(force_bytes(test_wrong_token))
        test_request_1 = self.factory.get('register/validation/')
        response_1 = ValidationView.as_view()(test_request_1, test_uid, test_utoken)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response_1.status_code, 200)
        print("ASSERT 1 DONE")
        print("self.assertInHTML(La page que vous recherchez n'existe pas, response_1.content.decode())")
        self.assertInHTML("La page que vous recherchez n'existe pas.", response_1.content.decode())
        print("ASSERT 2 DONE")


class UserStoriesAuthenticationTest(StaticLiveServerTestCase):
    """
    Authentication User stories: 4 user stories concerning the authentication part of the application.
    Selenium is used for the following tests.
    """
    fixtures = ['users.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox(options=firefox_options)
        cls.browser.implicitly_wait(10)
        cls.browser.maximize_window()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.quit()

    def test_login_when_registered(self):
        """
        Test the login process with an existing user.
        """
        print("\nTEST - SELENIUM --> TEST LOGIN WHEN REGISTERED\n")
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('log in').click()
        username_input = self.browser.find_element_by_css_selector('#id_username')
        username_input.send_keys("essai@email.fr")
        password_input = self.browser.find_element_by_css_selector('#id_password')
        password_input.send_keys("blabla75")
        self.browser.find_element_by_id('confirmer').click()
        print("assert 'Pas de message d'erreur concernant la saise des informations.' not in self.browser.page_source")
        assert 'Veuillez renseigner une adresse email et un mot de passe valides. Remarquez que chacun de ces champs est sensible à la casse (différenciation des majuscules/minuscules).' not in self.browser.page_source
        print("ASSERT DONE")

    def test_login_without_registered(self):
        """
        Test the login process with an non existing user.
        """
        print("\nTEST - SELENIUM --> TEST LOGIN WITHOUT REGISTERED\n")
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('log in').click()
        username_input = self.browser.find_element_by_css_selector('#id_username')
        username_input.send_keys("inconnu@gmail.fr")
        password_input = self.browser.find_element_by_css_selector('#id_password')
        password_input.send_keys("blabli95")
        self.browser.find_element_by_id('confirmer').click()
        print("assert 'Message d'erreur concernant la saise des informations.' in self.browser.page_source")
        assert 'Veuillez renseigner une adresse email et un mot de passe valides. Remarquez que chacun de ces champs est sensible à la casse (différenciation des majuscules/minuscules).' in self.browser.page_source
        print("ASSERT DONE")

    def test_login_then_logout(self):
        """
        Test the login process and logout with an existing user.
        """
        print("\nTEST - SELENIUM --> TEST LOGIN THEN LOGOUT\n")
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('log in').click()
        username_input = self.browser.find_element_by_css_selector('#id_username')
        username_input.send_keys("essai@email.fr")
        password_input = self.browser.find_element_by_css_selector('#id_password')
        password_input.send_keys("blabla75")
        self.browser.find_element_by_id('confirmer').click()
        self.browser.find_element_by_xpath('//*[@id="log out"]').click()
        print("assert 'Vous êtes déconnecté.' in self.browser.page_source")
        assert 'Vous êtes déconnecté.' in self.browser.page_source
        print("ASSERT DONE")

    def test_register_and_login_inactive(self):
        """
        Test the registration and login process without activating the account.
        """
        print("\nTEST - SELENIUM --> TEST REGISTER AND LOGIN INACTIVE\n")
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_xpath('//*[@id="page"]/div[2]/header/div/div/div[2]/a[2]/p/u').click()
        self.browser.find_element_by_xpath('//*[@id="id_first_name"]').send_keys('essai')
        self.browser.find_element_by_xpath('//*[@id="id_last_name"]').send_keys('TEST')
        self.browser.find_element_by_xpath('//*[@id="id_email"]').send_keys('essai@fauxemail.fr')
        self.browser.find_element_by_xpath('//*[@id="id_password1"]').send_keys('sUp€rpAssw0rd')
        self.browser.find_element_by_xpath('//*[@id="id_password2"]').send_keys('sUp€rpAssw0rd')
        self.browser.find_element_by_xpath('//*[@id="page"]/div[2]/div/div/div/form/button').click()
        print("assert 'Validation d'inscription en cours' in self.browser.page_source")
        assert "Validation d'inscription en cours" in self.browser.page_source
        print('ASSERT 1 DONE')
        self.browser.find_element_by_xpath('//*[@id="log in"]').click()
        self.browser.find_element_by_css_selector('#id_username').send_keys('essai@fauxemail.fr')
        self.browser.find_element_by_css_selector('#id_password').send_keys('sUp€rpAssw0rd')
        self.browser.find_element_by_id('confirmer').click()
        print("assert 'Veuillez valider votre compte en cliquant sur le lien reçu par courriel pour vous connecter.' in self.browser.page_source")
        assert 'Veuillez valider votre compte en cliquant sur le lien reçu par courriel pour vous connecter.' in self.browser.page_source
        print('ASSERT 2 DONE')

    def test_register_and_login_active(self):
        """
        Test the registration and login process when activating the account.
        """
        print("\nTEST - SELENIUM --> TEST REGISTER AND LOGIN ACTIVE\n")
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_xpath('//*[@id="page"]/div[2]/header/div/div/div[2]/a[2]/p/u').click()
        self.browser.find_element_by_xpath('//*[@id="id_first_name"]').send_keys('essai')
        self.browser.find_element_by_xpath('//*[@id="id_last_name"]').send_keys('TEST')
        self.browser.find_element_by_xpath('//*[@id="id_email"]').send_keys('essai@fauxemail.fr')
        self.browser.find_element_by_xpath('//*[@id="id_password1"]').send_keys('sUp€rpAssw0rd')
        self.browser.find_element_by_xpath('//*[@id="id_password2"]').send_keys('sUp€rpAssw0rd')
        self.browser.find_element_by_xpath('//*[@id="page"]/div[2]/div/div/div/form/button').click()
        print("assert 'Validation d'inscription en cours' in self.browser.page_source")
        assert "Validation d'inscription en cours" in self.browser.page_source
        print('ASSERT 1 DONE')
        test_user = User.objects.get(email='essai@fauxemail.fr')
        test_token = test_user.registration_token
        encoded_email = urlsafe_base64_encode(force_bytes('essai@fauxemail.fr'))
        encoded_token = urlsafe_base64_encode(force_bytes(test_token))
        test_url = self.live_server_url
        test_link = str(test_url) + '/user/register/validation/' + str(encoded_email) + '/' + str(encoded_token)
        self.browser.get(test_link)
        print("assert 'Vous êtes maintenant enregistré, bienvenue !' in self.browser.page_source")
        assert 'Vous êtes maintenant enregistré, bienvenue !' in self.browser.page_source
        print("ASSERT 2 DONE")
        self.browser.find_element_by_xpath('//*[@id="log in"]').click()
        self.browser.find_element_by_css_selector('#id_username').send_keys('essai@fauxemail.fr')
        self.browser.find_element_by_css_selector('#id_password').send_keys('sUp€rpAssw0rd')
        self.browser.find_element_by_id('confirmer').click()
        print("assert 'Pas de message d'erreur concernant la saise des informations.' not in self.browser.page_source")
        assert 'Veuillez renseigner une adresse email et un mot de passe valides. Remarquez que chacun de ces champs est sensible à la casse (différenciation des majuscules/minuscules).' not in self.browser.page_source
        print("ASSERT DONE")

    def test_change_password_when_logged_in(self):
        """
        Test the password modification process when logged in.
        """
        print("\nTEST - SELENIUM --> TEST CHANGE PASSWORD WHEN LOGGED IN\n")
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('log in').click()
        username_input = self.browser.find_element_by_css_selector('#id_username')
        username_input.send_keys("essai@email.fr")
        password_input = self.browser.find_element_by_css_selector('#id_password')
        password_input.send_keys("blabla75")
        self.browser.find_element_by_id('confirmer').click()
        self.browser.find_element_by_xpath('//*[@id="personal account"]').click()
        self.browser.find_element_by_xpath('//*[@id="page"]/div[2]/div[3]/div/a').click()
        self.browser.find_element_by_xpath('//*[@id="id_old_password"]').send_keys('blabla75')
        self.browser.find_element_by_xpath('//*[@id="id_new_password1"]').send_keys('sup€RpAssw0rd')
        self.browser.find_element_by_xpath('//*[@id="id_new_password2"]').send_keys('sup€RpAssw0rd')
        self.browser.find_element_by_xpath('//*[@id="confirmer"]').click()
        print("assert 'Mot de passe modifié' in self.browser.page_source")
        assert 'Mot de passe modifié' in self.browser.page_source
        print('ASSERT 1 DONE')
        self.browser.find_element_by_xpath('//*[@id="log out"]').click()
        self.browser.find_element_by_id('log in').click()
        self.browser.find_element_by_css_selector('#id_username').send_keys("essai@email.fr")
        self.browser.find_element_by_css_selector('#id_password').send_keys("sup€RpAssw0rd")
        self.browser.find_element_by_xpath('//*[@id="confirmer"]').click()
        print("assert 'Pas de message d'erreur concernant la saise des informations.' not in self.browser.page_source")
        assert 'Veuillez renseigner une adresse email et un mot de passe valides. Remarquez que chacun de ces champs est sensible à la casse (différenciation des majuscules/minuscules).' not in self.browser.page_source
        print("ASSERT 2 DONE")

    def test_reset_password_when_not_logged_in(self):
        """
        Test the password reset process when not logged in.
        """
        print("\nTEST - SELENIUM --> TEST RESET PASSWORD WHEN NOT LOGGED IN\n")
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('log in').click()
        self.browser.find_element_by_xpath('//*[@id="reset_password"]').click()
        self.browser.find_element_by_xpath('//*[@id="id_email"]').send_keys("essai@email.fr")
        self.browser.find_element_by_xpath('//*[@id="confirmer"]').click()
        print("assert 'Mot de passe oublié' in self.browser.page_source")
        assert 'Mot de passe oublié' in self.browser.page_source
        print('ASSERT 1 DONE')
        print("assert 'Un lien d'activation vient d'être envoyé à l'adresse demandée' in self.browser.page_source")
        assert "Un lien d'activation vient d'être envoyé à l'adresse demandée" in self.browser.page_source
        print('ASSERT 2 DONE')
        test_email_body = mail.outbox[0].body
        test_email_link = test_email_body.split(' ')[-2].split('\n')[-3]
        self.browser.get(test_email_link)
        self.browser.find_element_by_xpath('//*[@id="id_new_password1"]').send_keys("sup€RPassw0rd")
        self.browser.find_element_by_xpath('//*[@id="id_new_password2"]').send_keys("sup€RPassw0rd")
        self.browser.find_element_by_xpath('//*[@id="confirmer"]').click()
        print("assert 'Votre mot de passe a bien été modifié.' in self.browser.page_source")
        assert "Votre mot de passe a bien été modifié." in self.browser.page_source
        print('ASSERT 3 DONE')
        self.browser.find_element_by_id('log in').click()
        self.browser.find_element_by_css_selector('#id_username').send_keys("essai@email.fr")
        self.browser.find_element_by_css_selector('#id_password').send_keys("sup€RPassw0rd")
        self.browser.find_element_by_xpath('//*[@id="confirmer"]').click()
        print("assert 'Pas de message d'erreur concernant la saise des informations.' not in self.browser.page_source")
        assert 'Veuillez renseigner une adresse email et un mot de passe valides. Remarquez que chacun de ces champs est sensible à la casse (différenciation des majuscules/minuscules).' not in self.browser.page_source
        print("ASSERT 4 DONE")
