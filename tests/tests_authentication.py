from os import link
import time
from django.http import request
from django.test import TestCase, RequestFactory
from application.authentication.models import User
from application.authentication.views import RegisterView, ConsultAccountView
from application.authentication.forms import RegisterForm
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from unittest.mock import patch
from selenium import webdriver


firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = True

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
        self.user = User.objects.create_user(username='test',
                                             email='essai123@gmail.fr',
                                             password='lol175+essai')

    def test_consultaccountview_get(self):
        print("\nTEST - CONSULTACCOUNTVIEW --> def get()\n")
        request = self.factory.get('account/', )
        request.user = self.user
        response = ConsultAccountView.as_view()(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print('Assert Done')


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
        # self.browser.maximize_window()
        self.browser.find_element_by_id('log in').click()
        username_input = self.browser.find_element_by_css_selector('#id_username')
        username_input.send_keys("victor@gmail.fr")
        password_input = self.browser.find_element_by_css_selector('#id_password')
        password_input.send_keys("blabla75")
        self.browser.find_element_by_id('confirmer').click()
        print("assert 'Pas de message d'erreur concernant la saise des informations.' not in self.browser.page_source")
        assert 'Saisissez un email et un mot de passe valides. Remarquez que chacun de ces champs est sensible à la casse (différenciation des majuscules/minuscules).' not in self.browser.page_source
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
        assert 'Veuillez renseigner une adresse email et un mot de passe valide.' in self.browser.page_source
        print("ASSERT DONE")

    def test_login_then_logout(self):
        """
        Test the login process and logout with an existing user.
        """
        print("\nTEST - SELENIUM --> TEST LOGIN THEN LOGOUT\n")
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('log in').click()
        username_input = self.browser.find_element_by_css_selector('#id_username')
        username_input.send_keys("victor@gmail.fr")
        password_input = self.browser.find_element_by_css_selector('#id_password')
        password_input.send_keys("blabla75")
        self.browser.find_element_by_id('confirmer').click()
        self.browser.find_element_by_xpath('//*[@id="log out"]').click()
        print("assert 'Vous êtes déconnecté.' in self.browser.page_source")
        assert 'Vous êtes déconnecté.' in self.browser.page_source
        print("ASSERT DONE")
