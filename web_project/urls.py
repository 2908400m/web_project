"""web_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from drop_the_beat import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home,name = 'home'),
    path('drop_the_beat/', include('drop_the_beat.urls')),
    path('admin/', admin.site.urls),
    path('artists/', views.artists, name='artists'),
    path('artist/<int:artist_id>/', views.artist_detail, name='artist_detail'),
    path('song/<int:song_id>/', views.song, name='song'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
