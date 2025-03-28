# to run tests run "coverage run --source='.' manage.py test drop_the_beat"
# in the terminal. then run "coverage report" afterwards to check the coverage
# of the tests for the project
#

import sys
import os

from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from drop_the_beat.models import UserProfile, Artist, Song, Genre

from drop_the_beat.apps import DropTheBeatConfig

from drop_the_beat.forms import *

import importlib


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import populate_db
import population_script



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
        artist = Artist.objects.create(name="Lana del Slay")

        response = self.client.get(reverse('drop_the_beat:artists'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'drop_the_beat/artists.html')

        artist.delete()

    def test_addSong_view(self):
        test_user = User.objects.create_user(username='testbro', password='passbro')
        self.client.login(username='testbro', password='passbro')

        response = self.client.get(reverse('drop_the_beat:addSong'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'drop_the_beat/addSong.html')

        test_user.delete()


    def test_view_user_login_invalid(self):
        response = self.client.post(reverse('drop_the_beat:login'), {'username': 'no username', 'password': 'no password as well lol'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid login details')
    

    def test_signUp_view_GET(self):
        response = self.client.get(reverse('drop_the_beat:signUp'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'drop_the_beat/signUp.html')


    def test_signUp_view_POST(self):
        test_genre = Genre.objects.create(genre="pop")

        response = self.client.post(reverse('drop_the_beat:signUp'), {
            'username': 'user1221',
            'password': 'password',
            'bio': 'i forgot',
            'favorite_genre': test_genre.id
        })

        self.assertEqual(response.status_code, 200)

        test_genre.delete()


    def test_song_view_get(self):
        test_user = User.objects.create(username="user_number_million")
        test_profile = UserProfile.objects.create(user=test_user)
        test_genre = Genre.objects.create(genre="Pop")
        test_artist = Artist.objects.create(name="artist404")
        test_song = Song.objects.create(title="song about saying hi", artist=test_artist, genre=test_genre, uploaded_user=test_profile)

        url = reverse('drop_the_beat:song', args=[test_song.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'drop_the_beat/song.html')

        # delete all this after use
        test_user.delete()
        test_profile.delete()
        test_genre.delete()
        test_artist.delete()
        test_song.delete()




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


    def test_song_form_reuses_existing_artist(self):
        artist_existed_before = Artist.objects.create(name='Lana del Slay')

        # now adding a song with the existing creator BUT del in uppercase -- should be the same artist
        test_song = {'title': 'idk some song here', 'artist': 'lana DEL slay', 'genre': 'pop'}

        test_form = SongForm(data=test_song)
        self.assertTrue(test_form.is_valid())

        artist = test_form.cleaned_data['artist']
        self.assertEqual(artist, artist_existed_before)



class ModelTestsSTR(TestCase):
    def test_artist_model_str(self):
        test_artist = Artist.objects.create(name='Lana del Slay')
        self.assertEqual(str(test_artist), 'Lana del Slay')


    def test_genre_model_str(self):
        test_genre = Genre.objects.create(genre='Pop')
        self.assertEqual(str(test_genre), 'Pop')

    
    def test_song_model_str(self):
        test_user = User.objects.create(username='testuser')
        UserProfile.objects.create(user=test_user)

        test_artist = Artist.objects.create(name='Lana del Slay')
        test_genre = Genre.objects.create(genre='Pop')
        test_song = Song.objects.create(title='test song title', artist=test_artist, genre=test_genre)

        self.assertEqual(str(test_song), 'test song title')


    def test_user_profile_mofel_str(self):
        test_user = User.objects.create(username='testuser')
        test_profile = UserProfile.objects.create(user=test_user)

        self.assertIsInstance(test_profile.__str__(), User)


    def test_review_model_str(self):
        test_user = User.objects.create(username='testuser')
        UserProfile.objects.create(user=test_user)

        test_artist = Artist.objects.create(name='Lana del Slay')
        test_genre = Genre.objects.create(genre='Pop')

        test_song = Song.objects.create(title='test song title', artist=test_artist, genre=test_genre)

        test_review = Review.objects.create(user=test_user, song=test_song, rating=5)

        self.assertEqual(str(test_review), "Review by testuser for test song title")



class WSGI_Test(TestCase):
    def test_wsgi(self):
        import web_project.wsgi     # this runs wsgi.py
        importlib.reload(web_project.wsgi)

        self.assertIsNotNone(web_project.wsgi.application)


class Populate_DBTests(TestCase):
    def test_populate_db(self):
        populate_db.populate()

        self.assertGreater(Artist.objects.count(), 0)
        self.assertGreater(Genre.objects.count(), 0)
        self.assertGreater(Song.objects.count(), 0)

    def test_add_user_profile_returns_correctly(self):
        result = populate_db.add_user_profile(
            user="user does nto exist",
            email="nouserhere@mytest.com",
            bio="lol no bio",
            user_image="",
            favourite_genre="Pop"
        )
        self.assertIsInstance(result, UserProfile)

    
    def test_add_artist_updates_artist(self):
        artist = Artist.objects.create(name="Lana del Test", bio="bio", image="", spotify_id="")
        new_artist = populate_db.add_artist(name="Lana del Test", bio="new bio hi there", image="image here", spotify_id="id here")

        self.assertEqual(new_artist.bio, "new bio hi there")

        artist.delete()


    def test_add_review_when_user_doesnt_exist(self):
        test_artist = Artist.objects.create(name="artist1")
        test_genre = Genre.objects.create(genre="genre1")
        test_user = User.objects.create(username="user1")
        test_profile = UserProfile.objects.create(user=test_user)

        Song.objects.create(
            title="p",
            artist=test_artist,
            genre=test_genre,
            spotify_track_id="",
            album_art="",
            album_name="",
            uploaded_user=test_profile
        )

        result = populate_db.add_review(
            user="user doesnt exist :((",
            song="no song either :(((",
            rating=1,
            comment="no comment......."
        )

        self.assertIsNone(result)

        test_artist.delete()
        test_genre.delete()
        test_user.delete()
        test_profile.delete()


    def test_search_song_on_spotify_returns_none(self):
        result = populate_db.search_song_on_spotify("Foo Fighters", "Everlong")
        self.assertIsNone(result)

    
    def test_add_review_song_does_not_exist(self):
        test_user = User.objects.create(username="hmm-gonna-review-something")
        UserProfile.objects.create(user=test_user)

        result = populate_db.add_review(
            user="hmm-gonna-review-something",
            song="song does not exist :))",
            rating=5,
            comment="hi"
        )
        self.assertIsNone(result)

        test_user.delete()



# copied tests for PopulationScriptPyTests from Populate_DBTests (just the class about this test)
# as they are identical -- no point rewriting

class PopulationScriptPyTests(TestCase):
    def test_population_script_populate_runs(self):
        population_script.populate()
        self.assertGreater(Artist.objects.count(), 0)
        self.assertGreater(Genre.objects.count(), 0)
        self.assertGreater(Song.objects.count(), 0)
    

    def test_add_user_profile_returns_correctly(self):
        result = population_script.add_user_profile(
            user="user does nto exist",
            email="nouserhere@mytest.com",
            bio="lol no bio",
            user_image="",
            favourite_genre="Pop"
        )
        self.assertIsInstance(result, UserProfile)

    
    def test_add_artist_updates_artist(self):
        artist = Artist.objects.create(name="Lana del Test", bio="bio", image="", spotify_id="")
        new_artist = population_script.add_artist(name="Lana del Test", bio="new bio hi there", image="image here", spotify_id="id here")

        self.assertEqual(new_artist.bio, "new bio hi there")

        artist.delete()


    def test_add_review_when_user_doesnt_exist(self):
        test_artist = Artist.objects.create(name="artist1")
        test_genre = Genre.objects.create(genre="genre1")
        test_user = User.objects.create(username="user1")
        test_profile = UserProfile.objects.create(user=test_user)

        Song.objects.create(
            title="p",
            artist=test_artist,
            genre=test_genre,
            spotify_track_id="",
            album_art="",
            album_name="",
            uploaded_user=test_profile
        )

        result = population_script.add_review(
            user="user doesnt exist :((",
            song="no song either :(((",
            rating=1,
            comment="no comment......."
        )

        self.assertIsNone(result)

        test_artist.delete()
        test_genre.delete()
        test_user.delete()
        test_profile.delete()


    def test_search_song_on_spotify_returns_none(self):
        result = population_script.search_song_on_spotify("Foo Fighters", "Everlong")
        self.assertIsNone(result)

    
    def test_add_review_song_does_not_exist(self):
        test_user = User.objects.create(username="hmm-gonna-review-something")
        UserProfile.objects.create(user=test_user)

        result = population_script.add_review(
            user="hmm-gonna-review-something",
            song="song does not exist :))",
            rating=5,
            comment="hi"
        )
        self.assertIsNone(result)

        test_user.delete()