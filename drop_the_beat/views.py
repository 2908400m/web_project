from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'drop_the_beat/home.html')

def about(request):
    return render(request, 'drop_the_beat/about.html')

def contact(request):
    return render(request, 'drop_the_beat/contact.html')

def addSong(request):
    return render(request, 'drop_the_beat/addSong.html')

def artists(request):
    return render(request, 'drop_the_beat/artists.html')

def genres(request):
    return render(request, 'drop_the_beat/genres.html')