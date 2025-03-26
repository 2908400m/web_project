import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')
django.setup()

from drop_the_beat.models import Artist, Genre, Review, UserProfile, Song 
from django.contrib.auth.models import User

def populate():
    artists = [
        {"name": "Taylor Swift", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Ariana Grande", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Foo Fighters", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Maroon 5", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Rihanna", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Kendrick Lamar", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Gracie Abrams", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Sabrina Carpenter", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Ed Sheeran", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Jay Z", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"},
        {"name": "Katy Perry", "bio": "enter bio", "image": "enter image url", "spotify_id": "enter spotify id"}
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
        {"title": "Shake It Off", "artist": "Taylor Swift", "genre": "pop", "spotify_track_id": "enter track id", "album_art": "enter album art url"},
        {"title": "Not Like Us", "artist": "Kendrick Lamar", "genre": "rap", "spotify_track_id": "enter track id", "album_art": "enter album art url"},
        {"title": "No Tears Left To Cry", "artist": "Ariana Grande", "genre": "pop", "spotify_track_id": "enter track id", "album_art": "enter album art url"},
        {"title": "we can't be friends", "artist": "Ariana Grande", "genre": "pop", "spotify_track_id": "enter track id", "album_art": "enter album art url"},
        {"title": "Breakin' Dishes", "artist": "Rihanna", "genre": "pop", "spotify_track_id": "enter track id", "album_art": "enter album art url"},
        {"title": "Firework", "artist": "Katy Perry", "genre": "pop", "spotify_track_id": "enter track id", "album_art": "enter album art url"},
        {"title": "Espresso", "artist": "Sabrina Carpenter", "genre": "pop", "spotify_track_id": "enter track id", "album_art": "enter album art url"},
        {"title": "Please Please Please", "artist": "Sabrina Carpenter", "genre": "pop", "spotify_track_id": "enter track id", "album_art": "enter album art url"},
        {"title": "The Pretender", "artist": "Foo Fighters", "genre": "rock", "spotify_track_id": "enter track id", "album_art": "enter album art url"},
        {"title": "Shape Of You", "artist": "Ed Sheeran", "genre": "pop", "spotify_track_id": "enter track id", "album_art": "enter album art url"}
    ]


    for user_data in user_profiles:
        add_user_profile(user_data["user"], user_data["bio"], user_data["user_image"], user_data["favourite_genre"], user_data["email"])


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

    # for profile_data in user_profiles:
    #     add_user_profile(**profile_data)

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
        print(f"Error: Song '{song.title}' does not exist.")
        return None

def add_user_profile(user, bio, user_image, favourite_genre, email):
    genre, _ = Genre.objects.get_or_create(genre=favourite_genre)
    user_profile, created = UserProfile.objects.get_or_create(
        user=user, defaults={"bio": bio, "favorite_genre": genre, "profile_picture": user_image, "email": email}
    )
    return user_profile

if __name__ == '__main__':
    print("Populating database...")
    populate()
