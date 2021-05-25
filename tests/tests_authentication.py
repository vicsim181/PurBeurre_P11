import time
from django.test import TestCase, RequestFactory
from application.authentication.models import User
from application.authentication.views import RegisterView, ConsultAccountView
from application.authentication.forms import RegisterForm
from unittest.mock import patch
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
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
        self.user_test.set_password('blabla75')
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
    Test class for AuthenticationView.
    """
    def setUp(self):
        self.factory = RequestFactory()

    def test_registerview_get(self):
        print("\nTEST - REGISTERVIEW --> def get()\n")
        request = self.factory.get('register/', )
        response = RegisterView.as_view()(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print('Assert Done')

    @patch('application.authentication.views.RegisterView.form_class', autospec=RegisterForm)
    def test_registerview_post(self, mocked_form_class):
        mocked_form_class.is_valid.return_value = True
        request = self.factory.post('register/', data={})
        response = RegisterView.as_view()(request)
        self.assertEqual(response.status_code, 302)


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

    # def test_register(self):
    #     """
    #     Test the registration process by creating a new user.
    #     """
    #     print("\nTEST - SELENIUM --> TEST REGISTER\n")
    #     self.browser.get(self.live_server_url)
    #     self.browser.maximize_window()
    #     self.browser.find_element_by_id('log in').click()
    #     self.browser.find_element_by_id('register').click()
    #     self.browser.find_element_by_xpath('//*[@id="id_first_name"]').send_keys('essai')
    #     self.browser.find_element_by_xpath('//*[@id="id_last_name"]').send_keys('TEST')
    #     self.browser.find_element_by_xpath('//*[@id="id_email"]').send_keys('essai@gmail.com')
    #     self.browser.find_element_by_css_selector('#id_password1').send_keys('lala+89@')
    #     self.browser.find_element_by_css_selector('#id_password2').send_keys('lala+89@')
    #     button = self.browser.find_element_by_xpath('//*[@id="page"]/div[2]/div/div/div/form/button')
    #     self.browser.execute_script("arguments[0].click();", button)
    #     print("assert 'Veuillez renseigner ce champ.' in self.browser.page_source")
    #     assert 'Veuillez renseigner ce champ.' in self.browser.page_source
    #     print("ASSERT DONE")

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
        # self.browser.maximize_window()
        self.browser.find_element_by_id('log in').click()
        username_input = self.browser.find_element_by_css_selector('#id_username')
        username_input.send_keys("inconnu@gmail.fr")
        password_input = self.browser.find_element_by_css_selector('#id_password')
        password_input.send_keys("blabli95")
        self.browser.find_element_by_id('confirmer').click()
        print("assert 'Message d'erreur concernant la saise des informations.' in self.browser.page_source")
        assert 'Saisissez un email et un mot de passe valides. Remarquez que chacun de ces champs est sensible à la casse (différenciation des majuscules/minuscules).' in self.browser.page_source
        print("ASSERT DONE")

    def test_login_then_logout(self):
        """
        Test the login process and logout with an existing user.
        """
        print("\nTEST - SELENIUM --> TEST LOGIN THEN LOGOUT\n")
        self.browser.get(self.live_server_url)
        # self.browser.maximize_window()
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
