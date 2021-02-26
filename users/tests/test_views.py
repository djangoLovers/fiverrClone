from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from time import time
UserProfile = get_user_model()


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserProfile.objects.create(
            id=20,
            first_name='aydin',
            last_name='jabary',
            fullName='aydinjabary',
            username='aydinjabary',
            password='Apple8843'
        )
        self.user.save()

    def test_showGet(self):
        response = self.client.get(reverse('users:show', args=[self.user.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/show.html')

    def test_editGet(self):
        self.client.login(username='aydinjabary', password='Apple8843')
        response = self.client.get(reverse('users:edit', args=[self.user.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit.html')
