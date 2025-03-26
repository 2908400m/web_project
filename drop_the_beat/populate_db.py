import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')
django.setup()

from django.contrib.auth.models import User
from .models import Artist, Genre, Review, UserProfile, Song

def populate():
    artists = [
        {"name": "Olly Murs", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Doechii", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Ariana Venti", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Lana del Slay", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Pixie Chickies", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Taylor Swift", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Dustin Binspin", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Kendrick Lamar", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Rock My Socks", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
    ]

    genres = [
        {"genre": "pop"},
        {"genre": "rap"},
        {"genre": "rock"},
    ]

    reviews = [
        {"user": "enter username", "song": "enter song", "rating": "enter rating", "comment": "enter comment"},
        {"user": "enter username", "song": "enter song", "rating": "enter rating", "comment": "enter comment"},
        {"user": "enter username", "song": "enter song", "rating": "enter rating", "comment": "enter comment"},
        {"user": "enter username", "song": "enter song", "rating": "enter rating", "comment": "enter comment"}
    ]

    user_profiles = [
        {"user": "enter username", "bio": "enter bio", "user_image": "enter image url", "favourite_genre": "enter genre"},
        {"user": "enter username", "bio": "enter bio", "user_image": "enter image url", "favourite_genre": "enter genre"},
        {"user": "enter username", "bio": "enter bio", "user_image": "enter image url", "favourite_genre": "enter genre"}
    ]

    songs = [
        {"title": "enter title", "artist": "enter artist", "genre": "enter genre", "spotify_track_id": "enter track id", "album_art": "enter album art url"},
        {"title": "enter title", "artist": "enter artist", "genre": "enter genre", "spotify_track_id": "enter track id", "album_art": "enter album art url"},
        {"title": "enter title", "artist": "enter artist", "genre": "enter genre", "spotify_track_id": "enter track id", "album_art": "enter album art url"},
        {"title": "enter title", "artist": "enter artist", "genre": "enter genre", "spotify_track_id": "enter track id", "album_art": "enter album art url"},
        {"title": "enter title", "artist": "enter artist", "genre": "enter genre", "spotify_track_id": "enter track id", "album_art": "enter album art url"},
        {"title": "enter title", "artist": "enter artist", "genre": "enter genre", "spotify_track_id": "enter track id", "album_art": "enter album art url"},
        {"title": "enter title", "artist": "enter artist", "genre": "enter genre", "spotify_track_id": "enter track id", "album_art": "enter album art url"},
        {"title": "enter title", "artist": "enter artist", "genre": "enter genre", "spotify_track_id": "enter track id", "album_art": "enter album art url"},
        {"title": "enter title", "artist": "enter artist", "genre": "enter genre", "spotify_track_id": "enter track id", "album_art": "enter album art url"},
        {"title": "enter title", "artist": "enter artist", "genre": "enter genre", "spotify_track_id": "enter track id", "album_art": "enter album art url"}
    ]

    for artist_data in artists:
        add_artist(**artist_data)

    for genre_data in genres:
        add_genre(genre_data["genre"])

    for song_data in songs:
        add_song(
        song_data["title"],
        song_data["artist"], 
        song_data["genre"],  
        song_data["spotify_track_id"],
        song_data["album_art"]
    )

    for review_data in reviews:
        add_review(**review_data)

    for profile_data in user_profiles:
        add_user_profile(**profile_data)
    
    print("Database populated successfully!")

def add_artist(name, bio, image, spotify_id):
    artist, created = Artist.objects.get_or_create(
        name=name, defaults={"bio": bio, "image": image, "spotify_id": spotify_id}
    )
    return artist

def add_genre(name):
    genre, created = Genre.objects.get_or_create(genre=name)
    return genre

def add_song(title, artist_name, genre_name, spotify_track_id, album_art):
    artist, _ = Artist.objects.get_or_create(name=artist_name)
    genre, _ = Genre.objects.get_or_create(genre=genre_name)
    song, created = Song.objects.get_or_create(
        title=title, artist=artist, genre=genre,
        defaults={"spotify_track_id": spotify_track_id, "album_art": album_art}
    )
    return song

def add_review(user, song, rating, comment):
    try:
        user_obj = User.objects.get(username=user)  # Get the actual user object
        song = Song.objects.get(title=song)
        review, created = Review.objects.get_or_create(
            user=user_obj, song=song, defaults={"rating": rating, "comment": comment}
        )
        return review
    except User.DoesNotExist:
        print(f"Error: User '{user}' does not exist.")
        return None
    except Song.DoesNotExist:
        print(f"Error: Song '{song_title}' does not exist.")
        return None

def add_user_profile(user, bio, user_image, favourite_genre):
    try:
        user_obj = User.objects.get(username=user)  # Get the actual user object
    except User.DoesNotExist:
        print(f"Error: User '{user}' does not exist.")
        return None

    genre, _ = Genre.objects.get_or_create(genre=favourite_genre)
    user_profile, created = UserProfile.objects.get_or_create(
        user=user_obj, defaults={"bio": bio, "user_image": user_image, "favourite_genre": genre}
    )
    return user_profile

if __name__ == '__main__':
    print("Populating database...")
    populate()
