from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from drop_the_beat.forms import UserForm, UserProfileForm
from django.shortcuts import render, get_object_or_404
from .models import Artist
from .forms import SongForm, ReviewForm

def home(request):
    return render(request, 'drop_the_beat/home.html')

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
            song = song_form.save()

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
    return render(request, 'drop_the_beat/genres.html')

def rock(request):
    return render(request, 'drop_the_beat/rock.html')

def pop(request):
    return render(request, 'drop_the_beat/pop.html')

def rap(request):
    return render(request, 'drop_the_beat/rap.html')

def artists(request):
    all_artists = Artist.objects.all() 
    return render(request, 'drop_the_beat/artists.html', {'artists': all_artists})

def artist_detail(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)  
    songs = artist.songs.all()  
    return render(request, 'drop_the_beat/artist_detail.html', {'artist': artist, 'songs': songs})

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