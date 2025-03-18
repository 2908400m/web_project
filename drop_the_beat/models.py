from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)
    bio = models.TextField(blank = True)
    image = models.ImageField(upload_to="artist_image/", blank=True)
    profile_views = models.PositiveIntegerField(default=0)
    # spotify_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Genre(models.Model):
    genre = models.CharField(choices=[('pop', 'Pop'), ('rock', 'Rock'), ('rap', 'Rap')], max_length=100)

    def __str__(self):
        return self.genre

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="songs")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="genre_songs")
    # spotify_track_id= models.CharField(max_length=255)
    # song_preview_url= models.URLField()
    # album_art = models.URLField()

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True)
    favorite_genre = models.ForeignKey(Genre, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.user.username
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(choices=[(1, "1"),(2, "2"),(3, "3"),(4, "4"),(5, "5")], default=5)  
    comment = models.TextField(max_length=255, blank = True)

    class Meta:
        unique_together = ("user", "song")

    def __str__(self):
        return f"Review by {self.user.username} for {self.song.title}"