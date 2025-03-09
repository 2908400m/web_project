from django.contrib import admin
from .models import Artist, Genre, Song, UserProfile, Review

admin.site.register(Artist)

admin.site.register(Genre)

admin.site.register(Song)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'favorite_genre')
    search_fields = ('user__username', 'user__email', 'bio')

admin.site.register(UserProfile, UserProfileAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'song', 'rating', 'comment')
    search_fields = ('user__user__username', 'song__title', 'comment')

admin.site.register(Review, ReviewAdmin)
