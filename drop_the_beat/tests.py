# to run tests run "coverage run --source='.' manage.py test drop_the_beat"
# in the terminal. then run "coverage report" afterwards to check the coverage
# of the tests for the project
#


from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from drop_the_beat.models import UserProfile, Artist, Song, Genre

from drop_the_beat.apps import DropTheBeatConfig

# 
# from drop_the_beat.views import user_login
# from drop_the_beat.views import home

from drop_the_beat.forms import *

from drop_the_beat import populate_db

import importlib


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



class AppsTests(TestCase):
    def test_app_name(self):
        self.assertEquals(DropTheBeatConfig.name, 'drop_the_beat')
        # testing the name we get from the config is the one we want to use/are using



class ViewsPagesTests(TestCase):
    def test_homepage_view(self):
        response = self.client.get(reverse('drop_the_beat:home'))
        # test the status code and what template was used

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'drop_the_beat/home.html')


    def test_about_view(self):
        response = self.client.get(reverse('drop_the_beat:about'))
        # test the status code and what template was used

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'drop_the_beat/about.html')


    def test_contactpage_view(self):
        response = self.client.get(reverse('drop_the_beat:contact'))
        # test the status code and what template was used

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'drop_the_beat/contact.html')


    def test_genres_view(self):
        # creating a genre to test it
        genre = Genre.objects.create(genre="Pop")

        response = self.client.get(reverse('drop_the_beat:genres'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'drop_the_beat/genres.html')

        genre.delete()  # delete after use

    
    def test_genre_detail_view(self):
        # creating a genre to test it
        genre = Genre.objects.create(genre="Pop")

        response = self.client.get(reverse('drop_the_beat:genre_detail', args=[genre.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'drop_the_beat/genre.html')

        genre.delete()  # delete after use


    def test_artist_view(self):
        # creating an artist to test it
        artist = Artist.objects.create(name="Lana del Slay")

        response = self.client.get(reverse('drop_the_beat:artists'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'drop_the_beat/artists.html')

        artist.delete()


class FormsTests(TestCase):
    def test_form_is_valid(self):
        test_form_data = {'username': 'testuser', 'email': 'test@test.com', 'password': '123456'}
        test_form = UserForm(data=test_form_data)

        self.assertTrue(test_form.is_valid())
    

    def test_user_profile_is_valid(self):
        genre = Genre.objects.create(genre='Pop') # create a genre for testing

        test_profile_data = {'bio': 'i ♡ testing', 'favorite_genre': genre.id}
        test_form = UserProfileForm(data=test_profile_data)

        self.assertTrue(test_form.is_valid())

        genre.delete() # delete after use


    def test_form_cleaned_data(self):
        test_song = {'title': 'idk some song here', 'artist': 'Lana del Slay', 'genre': 'Pop'}
        test_form = SongForm(data=test_song)

        self.assertTrue(test_form.is_valid()) # first check that the form is valid

        # get clean_data from the form
        test_cleaned_artist = test_form.cleaned_data['artist']
        test_cleaned_genre = test_form.cleaned_data['genre']

        # test the cleaned data
        self.assertEqual(test_cleaned_artist.name, 'Lana del Slay')
        self.assertEqual(test_cleaned_genre.genre, 'pop')
        


class ModelTestsSTR(TestCase):
    def test_artist_model_str(self):
        test_artist = Artist.objects.create(name='Lana del Slay')
        self.assertEqual(str(test_artist), 'Lana del Slay')


    def test_genre_model_str(self):
        test_genre = Genre.objects.create(genre='Pop')
        self.assertEqual(str(test_genre), 'Pop')

    
    def test_song_model_str(self):
        test_artist = Artist.objects.create(name='Lana del Slay')
        test_genre = Genre.objects.create(genre='Pop')
        test_song = Song.objects.create(title='test song title', artist=test_artist, genre=test_genre)

        self.assertEqual(str(test_song), 'test song title')


    def test_user_profile_mofel_str(self):
        test_user = User.objects.create(username='testuser')
        test_profile = UserProfile.objects.create(user=test_user)

        self.assertEqual(str(test_profile), 'testuser')


    def test_review_model_str(self):
        test_user = User.objects.create(username='testuser')

        test_artist = Artist.objects.create(name='Lana del Slay')
        test_genre = Genre.objects.create(genre='Pop')

        test_song = Song.objects.create(title='test song title', artist=test_artist, genre=test_genre)

        test_review = Review.objects.create(user=test_user, song=test_song, rating=5)

        self.assertEqual(str(test_review), "Review by testuser for test song title")



class PopulateTest(TestCase):
    def test_populate(self): # the test passes but the coverage doesn't change -- TO FIX
        populate_db.populate()

        self.assertGreater(Artist.objects.count(), 0)
        self.assertGreater(Genre.objects.count(), 0)
        self.assertGreater(Song.objects.count(), 0)


    def test_adding_user_when_user_doesnt_exist(self):
        result = populate_db.add_user_profile(
            user="the user does not exist lol",
            bio="some bio here",
            user_image="",
            favourite_genre="Pop",
        )

        self.assertIsNone(result)

    
    def test_add_review_when_no_user_exists(self):
        result = populate_db.add_review(
            user="no user here lol",
            song="random song",
            rating=5,
            comment="no user or song lol",
        )

        self.assertIsNone(result)



class WSGI_Test(TestCase):
    def test_wsgi(self):
        import web_project.wsgi     # this runs wsgi.py
        importlib.reload(web_project.wsgi)

        self.assertIsNotNone(web_project.wsgi.application)