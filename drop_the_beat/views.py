from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from drop_the_beat.forms import UserForm, UserProfileForm

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