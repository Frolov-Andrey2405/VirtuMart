from .models import Product, ProductCategory
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class IndexViewTestCase(TestCase):
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        print(response)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'VirtuMart')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    @classmethod
    def setUpTestData(cls):
        cls.products = Product.objects.all()

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertListEqual(
            list(response.context['object_list']), list(self.products[:3]))

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse(
            'products:category', kwargs={
                'category_id': category.id})
        response = self.client.get(path)

        self._common_tests(response)
        self.assertListEqual(
            list(response.context['object_list']),
            list(self.products.filter(category_id=category.id))
        )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.context['title'], 'Catalog')
        self.assertTemplateUsed(response, 'products/products.html')
