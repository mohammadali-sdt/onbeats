from django.contrib import admin
from .models import Album, Artist, Song, Style

# Register your models here.


admin.site.register(Song)


class StyleInline(admin.StackedInline):
    model = Style


class SongInline(admin.StackedInline):
    model = Song


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    inlines = [
        StyleInline,
    ]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    inlines = [
        SongInline,
    ]
    prepopulated_fields = {'slug': ('name',)}
