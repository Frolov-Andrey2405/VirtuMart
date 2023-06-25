from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import Product, ProductCategory


class IndexViewTestCase(TestCase):
    '''
    Test case for the index view.
    '''
    def test_view(self):
        """
        The test_view function tests the view for the index page.
        It checks that:
            1) The response status code is 200 (HTTPStatus.OK).
            2) The title of the page is 'VirtuMart'.
            3) The correct template was used to render this view.
        """
        path = reverse('index')
        response = self.client.get(path)
        print(response)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'VirtuMart')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    '''
    Test case for the products list view.
    '''
    fixtures = ['categories.json', 'goods.json']

    @classmethod
    def setUpTestData(cls):
        """
        The setUpTestData function is run once, before any of the test methods are executed.
        It sets up a few products that can be used in all the test methods.
        """
        cls.products = Product.objects.all()

    def test_list(self):
        """
        The test_list function tests the products:index view.
        It checks that the response is a 200 OK, and that it uses
        the correct template. It also checks that there are 3 items in 
        the context, and they are all instances of Product.
        """
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertListEqual(
            list(response.context['object_list']), list(self.products[:3]))

    def test_list_with_category(self):
        """
        The test_list_with_category function tests the category view.
        It does this by creating a ProductCategory object, then using that to create a path for the test client to use.
        The response is then tested with _common_tests and assertListEquals functions.
        """
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
        """
        The _common_tests function is a helper function that tests the common elements of all views.
        It checks for an HTTP status code of 200, and it also checks to make sure that the title and template are correct.
        """
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.context['title'], 'Catalog')
        self.assertTemplateUsed(response, 'products/products.html')
