# python manage.py test - searches and runs test files
from unittest import skip  # facility to skip test

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from store.models import Category, Product
from store.views import all_products

# @skip("demonstrating skipping")
# class TestSkip(TestCase):
#     def test_skip_example(self):
#         pass


class TestViewResponses(TestCase):

    def setUp(self) -> None:
        self.c = Client()
        self.factory =  RequestFactory()

        self.category = Category.objects.create(name='django', slug='django')
        self.user = User.objects.create(username='john')
        self.product = Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                                            slug='django-beginners', price='20.00', image='django')

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
        Test product response status
        """
        # print("DATA: ", reverse('store:product_detail', args=['django-beginners']))
        response = self.c.get(reverse('store:product_detail', args=['django-beginners']))
        self.assertEqual(response.status_code, 200)


    def test_category_detail_url(self):
        """
        Test Category response status
        """
        # print("DATA-2: ", self.category.slug)
        response = self.c.get(reverse('store:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)

    
    def test_homepage_html(self):
        request = HttpRequest()
        response = all_products(request)
        html = response.content.decode('utf8')
        # print(html)
        self.assertIn('<title>BookStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    
    def test_view_function(self):
        request = self.factory.get('/item/django-beginners')
        response = all_products(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>BookStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)