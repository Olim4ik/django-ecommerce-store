from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.models import Category, Product


class TestBasketView(TestCase):

    def setUp(self):
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='john')
        Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                               slug='django-beginners', price='20.00', image='django')
        Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                               slug='django-beginners', price='20.00', image='django')
        Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                               slug='django-beginners', price='20.00', image='django')

        self.client.post(reverse('store_basket:basket_add'), {
                        "productid": 1, "productqty": 1, "action": "post"}, xhr=True)
        self.client.post(reverse('store_basket:basket_add'), {
                        "productid": 2, "productqty": 2, "action": "post"}, xhr=True)

    def test_basket_url(self):
        """
        Test homepage response status
        """
        response = self.client.get(reverse('store_basket:basket_summary'))
        
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        """
        Test adding items to the basket
        """
        # add item test
        response = self.client.post(
            reverse('store_basket:basket_add'), 
            {"productid": 3, "productqty": 1, "action": "post"},
            xhr=True
        )
        self.assertEqual(response.json(), {'qty': 4})

        # decrease already created item test
        response = self.client.post(
            reverse('store_basket:basket_add'), 
            {"productid": 2, "productqty": 1, "action": "post"},
            xhr=True
        )
        self.assertEqual(response.json(), {'qty': 3})

    def test_basket_udpate(self):
        """
        Test updating items from the basket
        """
        response = self.client.post(
            reverse('store_basket:basket_update'), 
            {"productid": 2, "productqty": 1, "action": "post"},
            xhr=True
        )
        self.assertEqual(response.json(), {'qty': 2, 'subtotal': '40.00'})

    def test_basket_delete(self):
        """
        Test deleting items from the basket
        """
        response = self.client.post(
            reverse('store_basket:basket_delete'), 
            {"productid": 2, "action": "post"},
            xhr=True
        )
        self.assertEqual(response.json(), {'qty': 1, 'subtotal': '20.00'})
