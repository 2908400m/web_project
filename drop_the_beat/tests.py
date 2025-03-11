from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from .models import Artist, Song

class HomepageTests(TestCase):
    def test_homepage(self):
        response = self.client.get(reverse('drop_the_beat:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'drop_the_beat/home.html')


class ArtistDetailTests(TestCase):
    def test_artist_details(self):
        # creating an arrists and saving them
        self.artist = Artist.objects.create(name='Test Artist')

        url=reverse('drop_the_beat:artist_detail', args=[self.artist.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.artist.name)


class UserLoginLogoutTests(TestCase):
    def test_user_login(self):
        user = User.objects.create_user(username='testuser', password='testuser')
        response = self.client.post(reverse('drop_the_beat:login'), {'username': 'testuser', 'password': 'testuser'})

        self.assertEqual(response.status_code, 302) # successful redirect
        user.delete() # getting rid of the test user
    
    def test_user_logout(self):
        user = User.objects.create_user(username='testuser', password='testuser')
        self.client.login(username='testuser', password='testuser')
        response = self.client.get(reverse('drop_the_beat:logout'))

        self.assertEqual(response.status_code, 302) # successful redirect
        user.delete() # getting rid of the test user