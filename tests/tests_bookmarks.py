from application.bookmark.models import Substitution
from application.bookmark.views import BookmarksView
from application.authentication.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import RequestFactory, TestCase
from application.main.models import Product
# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.firefox.webdriver import WebDriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By


# firefox_options = webdriver.FirefoxOptions()
# firefox_options.headless = True

# Create your tests here.
class BookmarkTests(TestCase):
    """
    Test class holding the functions testing the Substitution model.
    """
    def setUp(self):
        self.product_source = Product(name="Coca-Cola Classic",
                                      code="5449000000996",
                                      nutriscore="e",
                                      url="https://fr.openfoodfacts.org/produit/5449000000996/coca-cola",
                                      popularity=2802)
        self.product_source.save()
        self.product_target = Product(name="Coca-Cola Zero",
                                      code="5449000133335",
                                      nutriscore="b",
                                      url="https://fr.openfoodfacts.org/produit/5449000133335/coca-cola-zero",
                                      popularity=181)
        self.product_target.save()
        test_user = User(email='essai@gmail.com', password=None, first_name='essai', last_name='register')
        test_user.set_password('blabla75')
        test_user.save()
        self.target_user = User.objects.get(email='essai@gmail.com')

    def test_save_and_get_bookmarks(self):
        print("\nTEST - Bookmark --> def save_bookmark()\n")
        Substitution.save_bookmark(self.product_source.id, self.product_target.id, self.target_user.id)
        print("TEST_BOOKMARK SAVED")
        print("\nTEST - Bookmark --> def get_bookmarks()\n")
        test_get_bookmarks = Substitution.get_bookmarks_by_user(self.target_user.id)
        print("self.assertTrue(test_get_bookmarks[0].target_product_id, self.product_target.id)")
        self.assertTrue(test_get_bookmarks[0].target_product_id, self.product_target.id)
        print('Assert 1 Done')
        print("self.assertTrue(test_get_bookmarks[0].source_product_id, self.product_source.id)")
        self.assertTrue(test_get_bookmarks[0].source_product_id, self.product_source.id)
        print('Assert 2 Done')

    def test_get_and_delete_bookmark(self):
        print("\nTEST - Bookmark --> def delete_bookmark()\n")
        Substitution.save_bookmark(self.product_source.id, self.product_target.id, self.target_user.id)
        print("TEST_BOOKMARK SAVED")
        test_delete_bookmark = Substitution.objects.get(
                               source_product_id=self.product_source.id,
                               target_product_id=self.product_target.id,
                               user_id=self.target_user.id)
        print("test_delete_bookmark.delete()")
        test_delete_bookmark.delete()
        print("\ndef get_bookmarks_by_user()\n")
        test_get_bookmarks = Substitution.get_bookmarks_by_user(self.target_user.id)
        print("self.assertQuerysetEqual(test_get_bookmarks, [])")
        self.assertQuerysetEqual(test_get_bookmarks, [])
        print('Assert 1 Done')

    def test_specific_bookmark(self):
        print("\nTEST - Bookmark --> def specific_bookmark()\n")
        Substitution.save_bookmark(self.product_source.id, self.product_target.id, self.target_user.id)
        test_specific_1 = Substitution.specific_bookmark(self.product_source.id, self.product_target.id, self.target_user.id)
        print("self.assertTrue(Substitution.specific_bookmark(self.product_source.id, self.product_target.id, self.target_user.id))")
        self.assertTrue(test_specific_1)
        print('ASSERT 1 DONE')
        print("self.assertFalse(Substitution.specific_bookmark(5620, 5621, 12))")
        test_specific_2 = Substitution.specific_bookmark(5620, 5621, 12)
        self.assertFalse(test_specific_2)
        print("ASSERT 2 DONE")

    def test_check_favs(self):
        print("\nTEST - Bookmark --> def check_favs()\n")
        Substitution.save_bookmark(self.product_source.id, self.product_target.id, self.target_user.id)
        test_favs = Substitution.check_favs(self.product_source, self.target_user)
        print('test_favs: ' + str(test_favs))
        print("self.assertEqual(Substitution.check_favs(self.product_source, self.target_user)[0], 2")
        self.assertEqual(test_favs[0], 2)
        print('ASSERT DONE')


class TestBookmarksView(TestCase):
    """
    Test class for BookmarksView.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test',
                                             email='essaitest@gmail.fr',
                                             password='essaimdp+88')
        product = Product(name="Coca cola 1L",
                          code="5449000054227",
                          nutriscore="e",
                          url="https://fr.openfoodfacts.org/produit/5449000054227/coca-cola",
                          popularity=561,)
        product.save()
        product = Product(name="Coca Zéro",
                          code="5449000133328",
                          nutriscore="b",
                          url="https://fr.openfoodfacts.org/produit/5449000133328/coca-zero-coca-cola",
                          popularity=538,)
        product.save()

    def test_bookmarksview_get(self):
        print("\nTEST - BOOKMARKSVIEW --> def get()\n")
        substitution = Substitution(source_product_id=Product.objects.get(code="5449000133328").id,
                                    target_product_id=Product.objects.get(code="5449000054227").id,
                                    user_id=self.user.id,)
        substitution.save()
        request = self.factory.get('consult/', )
        request.user = self.user
        response = BookmarksView.as_view()(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print('Assert Done')

    def test_bookmarksview_post(self):
        print("\nTEST - BOOKMARKSVIEW --> def post() --> add bookmark\n")
        data = {
            'aim': 'add',
            'current_user': self.user,
            'product_id': 11,
            'suggestion_id': 12,
        }
        request = self.factory.post('consult/', data)
        request.user = self.user
        BookmarksView.as_view()(request)
        bookmark_test = Substitution.objects.get(user_id=self.user.id)
        print("self.assertEqual(bookmark_test.source_product_id, 11)")
        self.assertEqual(bookmark_test.source_product_id, 11)
        print("ASSERT DONE")
        print("\nTEST - BOOKMARKSVIEW --> def post() --> delete bookmark\n")
        data = {
            'aim': 'delete',
            'current_user': self.user,
            'product_id': 11,
            'suggestion_id': 12,
        }
        request = self.factory.post('consult/', data)
        request.user = self.user
        response = BookmarksView.as_view()(request)
        bookmark_test = Substitution.objects.all()
        print("self.assertIsNone(bookmark_test)")
        self.assertQuerysetEqual(bookmark_test, [])
        print("ASSERT DONE")
        print("self.assertEqual(response, 302)")
        self.assertEqual(response.status_code, 302)
        print("ASSERT DONE")
        print("\nTEST - BOOKMARKSVIEW --> def post() --> empty 'aim'\n")
        data = {
            'aim': '',
            'current_user': self.user,
            'product_id': 11,
            'suggestion_id': 12,
        }
        request = self.factory.post('consult/', data)
        request.user = self.user
        BookmarksView.as_view()(request)
