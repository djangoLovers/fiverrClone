from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from time import time
from ..models import UserProfile


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        UserProfile.objects.create(
            id=1,
            Username='test',
            first_name='Aydin',
            last_name='Jabary',
            email='aydin@gmail.com',
            description='description',
            biography='test',
            dateCreated=time(),
            country='IR',
            image='/home/aydin/Pictures/test.jpg',
            password='123'
        )

    def test_showGet(self):
        response = self.client.get(reverse('users:show', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/show.html')

    def test_editGet(self):
        response = self.client.get(reverse('users:edit', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit.html')
