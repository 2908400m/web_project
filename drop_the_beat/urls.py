from django.urls import path
from drop_the_beat import views

app_name = 'drop_the_beat'

urlpatterns = [
    path('', views.home,name = 'home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('addSong/', views.addSong, name='addSong'),
    path('artists/', views.artists, name='artists'),
    path('genres/', views.genres, name='genres'),
    path('login/', views.user_login, name='login'),
    path('signUp/', views.signUp, name='signUp'),
    path('logout/', views.user_logout, name='logout'),
    path('artist/<int:artist_id>/', views.artist_detail, name='artist_detail'),
    path('genre/<int:genre_id>/', views.genre_detail, name='genre_detail'),
    path('song/<int:song_id>/', views.song, name='song'),
    


]
