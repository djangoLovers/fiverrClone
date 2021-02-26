from django.test import SimpleTestCase
from django.urls import reverse
from django.urls.base import resolve
from ..views import index, logout


class TestUrls(SimpleTestCase):
    def test_indexUrlIsResolved(self):
        url = reverse('core:index')
        self.assertEquals(resolve(url).func, index)

    def test_logoutUrlIsResolved(self):
        url = reverse('core:logout')
        self.assertEquals(resolve(url).func, logout)
