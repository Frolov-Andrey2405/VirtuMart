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
