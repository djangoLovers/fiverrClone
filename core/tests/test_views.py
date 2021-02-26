from django.test import TestCase, Client, client
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_indexGet(self):
        response = self.client.get(reverse('core:index'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_logoutGet(self):
        response = self.client.get(reverse('core:logout'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'logout.html')
