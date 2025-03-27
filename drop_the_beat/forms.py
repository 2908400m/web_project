from django import forms
from django.contrib.auth.models import User
from drop_the_beat.models import UserProfile
from .models import Song, Review, Artist, Genre


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_picture', 'favorite_genre')

class SongForm(forms.ModelForm):
    title = forms.CharField(label="Song Title", widget=forms.TextInput(attrs={'placeholder': 'Enter song title'}))
    artist = forms.CharField(label="Artist Name", widget=forms.TextInput(attrs={'placeholder': 'Enter artist name'}))
    genre = forms.CharField(label="Genre", widget=forms.TextInput(attrs={'placeholder': 'Enter genre'}))

    class Meta:
        model = Song
        fields = ['title', 'artist', 'genre']

    def clean_artist(self):
        artist_name = self.cleaned_data['artist'].strip()
        existing_artist = Artist.objects.filter(name__iexact=artist_name).first()
        
        if existing_artist:
            return existing_artist
        else:
            artist = Artist.objects.create(name=artist_name)
            
            return artist

    def clean_genre(self):
        genre_name = self.cleaned_data['genre'].lower()
        genre, _ = Genre.objects.get_or_create(genre=genre_name) 
        return genre  
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']