from django.test import SimpleTestCase
from django.urls import reverse
from django.urls.base import resolve
from ..views import index, show, new, edit, comment, order, callback, result, search


class TestUrls(SimpleTestCase):
    def test_indexUrlIsResolved(self):
        url = reverse('gigs:index')
        self.assertEquals(resolve(url).func, index)

    def test_showUrlIsResolved(self):
        url = reverse('gigs:show', args=[1])
        self.assertEquals(resolve(url).func, show)

    def test_newUrlIsResolved(self):
        url = reverse('gigs:new')
        self.assertEquals(resolve(url).func, new)

    def test_editUrlIsResolved(self):
        url = reverse('gigs:edit', args=[1])
        self.assertEquals(resolve(url).func, edit)

    def test_commentUrlIsResolved(self):
        url = reverse('gigs:comment', args=[1])
        self.assertEquals(resolve(url).func, comment)

    def test_orderUrlIsResolved(self):
        url = reverse('gigs:order', args=[1])
        self.assertEquals(resolve(url).func, order)

    def test_callbackUrlIsResolved(self):
        url = reverse('gigs:callback')
        self.assertEquals(resolve(url).func, callback)

    def test_resultUrlIsResolved(self):
        url = reverse('gigs:result')
        self.assertEquals(resolve(url).func, result)

    def test_searchUrlIsResolved(self):
        url = reverse('gigs:search')
        self.assertEquals(resolve(url).func, search)
