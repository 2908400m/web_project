import os
import django
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from collections import defaultdict
from dotenv import load_dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')
django.setup()

load_dotenv()

client_credentials_manager = SpotifyClientCredentials(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET')
)

from drop_the_beat.models import Artist, Genre, Review, UserProfile, Song 
from django.contrib.auth.models import User
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def populate():
    artists = [
        {"name": "Taylor Swift", "bio": "Taylor Alison Swift (born December 13, 1989) is an American singer-songwriter.", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Ariana Grande", "bio": "Ariana Grande-Butera born June 26, 1993) is an American singer, songwriter, and actress.", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Foo Fighters", "bio": "The Foo Fighters are an American rock band formed in Seattle in 1994.", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Maroon 5", "bio": "Maroon 5 is an American pop rock band from Los Angeles, California.", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Rihanna", "bio": "Robyn Rihanna Fenty, born February 20, 1988) is a Barbadian singer, businesswoman, and actress.", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Kendrick Lamar", "bio": "Kendrick Lamar Duckworth (born June 17, 1987) is an American rapper.", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Gracie Abrams", "bio": "Gracie Madigan Abrams (born September 7, 1999) is an American singer-songwriter and daughter of J. J. Abrams.", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Sabrina Carpenter", "bio": "Sabrina Annlynn Carpenter (born May 11, 1999) is an American singer, songwriter, and actress.", "image": "enter image url", "spotify_id": "enter spotify id"},    
        {"name": "Ed Sheeran", "bio": "Edward Christopher Sheeran (born 17 February 1991) is an English singer-songwriter.", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Jay Z", "bio": "Shawn Corey Carter (born December 4, 1969), known professionally as Jay-Z,[a] is an American rapper, businessman, and record executive.", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Katy Perry", "bio": "Katheryn Elizabeth Hudson (born October 25, 1984), known professionally as Katy Perry, is an American singer, songwriter, and television personality.", "image": "enter image url", "spotify_id": "enter spotify id"}
    ]

    genres = [
        {"genre": "pop"},
        {"genre": "rap"},
        {"genre": "rock"},
    ]

    user_profiles = [
        {"user": "johnsmith24", "bio": "enter bio", "user_image": "enter image url", "favourite_genre": "pop", "email":"enteremail"},
        {"user": "rebecca123", "bio": "enter bio", "user_image": "enter image url", "favourite_genre": "rock", "email":"enteremail"},
        {"user": "love_music94", "bio": "enter bio", "user_image": "enter image url", "favourite_genre": "rap", "email":"enteremail"}
    ]

    reviews = [
        {"user": "johnsmith24", "song": "Shape Of You", "rating": 1, "comment": "Not a fan of this"},
        {"user": "rebecca123", "song": "Firework", "rating": 3, "comment": "Meh, its ok"},
        {"user": "love_music94", "song": "Shape Of You", "rating": 4, "comment": "Really like this song"},
        {"user": "love_music94", "song": "Not Like Us", "rating": 5, "comment": "SO good!!!"}
    ]

    

    songs = [
        {"title": "Shake It Off", "artist": "Taylor Swift", "genre": "pop", "spotify_track_id": "enter track id", "album_art": "enter album art url", "uploaded_user": "rebecca123"},
        {"title": "Not Like Us", "artist": "Kendrick Lamar", "genre": "rap", "spotify_track_id": "enter track id", "album_art": "enter album art url", "uploaded_user": "love_music94"},
        {"title": "No Tears Left To Cry", "artist": "Ariana Grande", "genre": "pop", "spotify_track_id": "enter track id", "album_art": "enter album art url", "uploaded_user": "rebecca123"},
        {"title": "we can't be friends", "artist": "Ariana Grande", "genre": "pop", "spotify_track_id": "enter track id", "album_art": "enter album art url", "uploaded_user": "rebecca123"},
        {"title": "Breakin' Dishes", "artist": "Rihanna", "genre": "pop", "spotify_track_id": "enter track id", "album_art": "enter album art url", "uploaded_user": "love_music94"},
        {"title": "Firework", "artist": "Katy Perry", "genre": "pop", "spotify_track_id": "enter track id", "album_art": "enter album art url", "uploaded_user": "rebecca123"},
        {"title": "Espresso", "artist": "Sabrina Carpenter", "genre": "pop", "spotify_track_id": "enter track id", "album_art": "enter album art url", "uploaded_user": "love_music94"},
        {"title": "Please Please Please", "artist": "Sabrina Carpenter", "genre": "pop", "spotify_track_id": "enter track id", "album_art": "enter album art url", "uploaded_user": "johnsmith24"},
        {"title": "The Pretender", "artist": "Foo Fighters", "genre": "rock", "spotify_track_id": "enter track id", "album_art": "enter album art url", "uploaded_user": "johnsmith24"},
        {"title": "Shape Of You", "artist": "Ed Sheeran", "genre": "pop", "spotify_track_id": "enter track id", "album_art": "enter album art url", "uploaded_user": "johnsmith24"}
    ]


    for user_data in user_profiles:
        add_user_profile(user_data["user"], user_data["bio"], user_data["user_image"], user_data["favourite_genre"], user_data["email"])


    for artist_data in artists:
        add_artist(**artist_data)

    for genre_data in genres:
        add_genre(genre_data["genre"])

    for song_data in songs:

        user = UserProfile.objects.get(user=song_data["uploaded_user"])

        song = search_song_on_spotify(song_data["title"], song_data["artist"])
        add_song(
        song_data["title"],
        song_data["artist"], 
        song_data["genre"],  
        song["spotify_track_id"],
        song["cover_art"],
        song["album_name"],
        uploaded_user=user
    )

    print("Database populated successfully!")

def add_artist(name, bio, image, spotify_id):
    artist, created = Artist.objects.get_or_create(
        name=name, defaults={"bio": bio, "image": image, "spotify_id": spotify_id}
    )

    if not created:
        artist.bio=bio
        artist.save()

    return artist

def add_genre(name):
    genre, created = Genre.objects.get_or_create(genre=name)
    return genre

def add_song(title, artist_name, genre_name, spotify_track_id, album_art, album_name, uploaded_user):
    artist, _ = Artist.objects.get_or_create(name=artist_name)
    genre, _ = Genre.objects.get_or_create(genre=genre_name)
    song, created = Song.objects.get_or_create(
        title=title, artist=artist, genre=genre,
        defaults={"spotify_track_id": spotify_track_id, "album_art": album_art, "album_name": album_name, "uploaded_user":uploaded_user}
    )
    return song

def add_review(user, song, rating, comment):
    try:
        user_obj = UserProfile.objects.get(user=user)  # Get the actual user object
        song = Song.objects.get(title=song)
        
        rating = int(rating)
        review, created = Review.objects.get_or_create(
            user=user_obj, song=song, defaults={"rating": rating, "comment": comment}
        )
        return review
    except UserProfile.DoesNotExist:
        print(f"Error: User '{user}' does not exist.")
        return None
    except Song.DoesNotExist:
        print(f"Error: Song '{song.title}' does not exist.")
        return None

def add_user_profile(user, bio, user_image, favourite_genre, email):
    genre, _ = Genre.objects.get_or_create(genre=favourite_genre)
    user_profile, created = UserProfile.objects.get_or_create(
        user=user, defaults={"bio": bio, "favorite_genre": genre, "profile_picture": user_image, "email": email}
    )
    return user_profile

def search_song_on_spotify(title, artist_name):
    query = f"track:{title} artist:{artist_name}"
    results = spotify.search(q=query, limit=1, type="track")
    
    if results["tracks"]["items"]:
        track=results["tracks"]["items"][0]
    else:
        track=None

    if track:
        return{
            "title":track["name"],
            "artist_name":track["artists"][0]["name"],
            "spotify_track_id": track["id"],
            "cover_art":track["album"]["images"][0]["url"],
            "album_name":track["album"]["name"]
        }
    else:
        return None 

if __name__ == '__main__':  # pragma: no cover
    print("Populating database...")
    populate()
