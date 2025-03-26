import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')
django.setup()

from drop_the_beat.models import Artist, Genre, Review, UserProfile, Song 
from django.contrib.auth.models import User

def populate():
    artists = [
        {"name": "enter name", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "enter name", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "enter name", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "enter name", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "enter name", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "enter name", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "enter name", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "enter name", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "enter name", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "enter name", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "enter name", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"}
    ]

    genres = [
        {"genre": "pop"},
        {"genre": "rap"},
        {"genre": "rock"},
    ]

    reviews = [
        {"user": "enter4username", "song": "enter song", "rating": 1, "comment": "enter comment"},
        {"user": "enter3username", "song": "enter song", "rating": 3, "comment": "enter comment"},
        {"user": "enter2username", "song": "enter song", "rating": 4, "comment": "enter comment"},
        {"user": "enterusername", "song": "enter song", "rating": 5, "comment": "enter comment"}
    ]

    user_profiles = [
        {"user": "enterusername", "bio": "enter bio", "user_image": "enter image url", "favourite_genre": "enter genre"},
        {"user": "enter3username", "bio": "enter bio", "user_image": "enter image url", "favourite_genre": "enter genre"},
        {"user": "enter4username", "bio": "enter bio", "user_image": "enter image url", "favourite_genre": "enter genre"}
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

    users = [
    {"username": "enterusername", "email": "user1@example.com"},
    {"username": "enter2username", "email": "user2@example.com"},
    {"username": "enter3username", "email": "user3@example.com"}
    ]

    for user_data in users:
        User.objects.get_or_create(username=user_data["username"], defaults={"email": user_data["email"]})



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

    for profile_data in user_profiles:
        add_user_profile(**profile_data)

    for review_data in reviews:
        add_review(**review_data)
    
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
        user=user_obj, defaults={"bio": bio, "favorite_genre": genre}
    )
    return user_profile

if __name__ == '__main__':
    print("Populating database...")
    populate()
