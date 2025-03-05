from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def addSong(request):
    return render(request, 'addSong.html')

def artists(request):
    return render(request, 'artists.html')