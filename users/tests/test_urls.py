from django.test import SimpleTestCase
from django.urls import reverse
from django.urls.base import resolve
from ..views import show, edit, orders, sales


class TestUrls(SimpleTestCase):
    def test_showUrlIsResolved(self):
        url = reverse('users:show', args=[1])
        self.assertEquals(resolve(url).func, show)

    def test_editUrlIsResolved(self):
        url = reverse('users:edit', args=[1])
        self.assertEquals(resolve(url).func, edit)

    def test_ordersUrlIsResolved(self):
        url = reverse('users:orders', args=[1])
        self.assertEquals(resolve(url).func, orders)

    def test_salesUrlIsResolved(self):
        url = reverse('users:sales', args=[1])
        self.assertEquals(resolve(url).func, sales)
