from django.urls import path
from drop_the_beat import views

app_name = 'drop_the_beat'

urlpatterns = [
    path('', views.home,name = 'home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('addSong/', views.addSong, name='addSong'),
    path('artists/', views.artists, name='artists'),
]
