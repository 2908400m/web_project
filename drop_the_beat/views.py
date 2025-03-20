from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from drop_the_beat.forms import UserForm, UserProfileForm
from django.shortcuts import render, get_object_or_404
from .models import Artist, Song, Genre
from .forms import SongForm, ReviewForm
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from collections import defaultdict
from dotenv import load_dotenv, dotenv_values

load_dotenv()

client_credentials_manager = SpotifyClientCredentials(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET')
)

spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def home(request):
    popular_artists = Artist.objects.order_by('-profile_views')[:10]

    context = {
        'popular_artists': popular_artists
    }
    
    return render(request, 'drop_the_beat/home.html', context)

def about(request):
    return render(request, 'drop_the_beat/about.html')

def contact(request):
    return render(request, 'drop_the_beat/contact.html')

@login_required
def addSong(request):
    if request.method == "POST":
        song_form = SongForm(request.POST)
        review_form = ReviewForm(request.POST)

        if song_form.is_valid() and review_form.is_valid():

            title = song_form.cleaned_data["title"]
            artist = song_form.cleaned_data["artist"]
            genre = song_form.cleaned_data["genre"]

            song_data = search_song_on_spotify(title, artist)

            if song_data:
                artist = Artist.objects.get_or_create(name=song_data['artist_name'])[0]
                song = Song(
                    title=song_data["title"],
                    artist=artist,
                    genre=genre,
                    spotify_track_id=song_data["spotify_track_id"],
                    album_art=song_data["cover_art"],
                    album_name=song_data["album_name"]
                    )
                song.save()
            else:
                print(f"The song {title} by {artist} does not exist on spotify")
                return HttpResponse("The submitted song does not exist on spotify.")

            review = review_form.save(commit=False)
            review.song = song
            review.user = request.user 
            review.save()

            return redirect('artists') 

    else:
        song_form = SongForm()
        review_form = ReviewForm()

    return render(request, 'drop_the_beat/addSong.html', {
        'song_form': song_form,
        'review_form': review_form
    })


def genres(request):
    all_genres = Genre.objects.all()
    return render(request, 'drop_the_beat/genres.html', {'genres': all_genres})

def genre_detail(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    songs = genre.genre_songs.all()
    return render(request, 'drop_the_beat/genre.html', {'genre': genre, 'songs': songs})



def artists(request):
    all_artists = Artist.objects.all() 
    return render(request, 'drop_the_beat/artists.html', {'artists': all_artists})

def artist_detail(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)  
    artist.profile_views += 1
    artist.save()
    songs = artist.songs.all()  
    albums = defaultdict(list)
    for song in songs:
        albums[song.album_name].append(song)

    return render(request, 'drop_the_beat/artist_detail.html', {'artist': artist, 'songs': songs, 'albums':dict(albums)})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('home'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'drop_the_beat/login.html')
    
def signUp(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    

    return render(request, 'drop_the_beat/signUp.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('home'))

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

def song(request, song_id):
    song = get_object_or_404(Song, id=song_id) 
    return render(request, 'drop_the_beat/song.html', {'song': song})
