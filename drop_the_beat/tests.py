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

