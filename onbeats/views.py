from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from django.core import serializers
from .models import Artist, Album, Song
from .forms import UserRegistrationForm


# Create your views here.

def get_new_albums(request):
    # albums = Album.objects.values('name').order_by('-created_at')
    albums = Album.objects.order_by('-created_at')
    # return JsonResponse({'albums': list(albums)}, status=200)
    return render(request, 'onbeats/home.html', {'albums': albums})


def get_artist(request, artist_slug):
    artist = get_object_or_404(Artist, slug=artist_slug)
    # artist_albums = artist.albums.all().order_by('release_year').values(
    # 'name')
    return render(request, 'onbeats/artist.html', {'artist': artist})
    # return JsonResponse({'artist': artist.name, 'albums': list(
    # artist_albums)}, status=200)


def get_album_songs(request, album_slug):
    album = get_object_or_404(Album, slug=album_slug)

    return render(request, 'onbeats/album.html', {'album': album})


def get_all_artists(request):
    # artists = Artist.objects.values('name').order_by('name')
    artists = Artist.objects.all().order_by('name')
    # return JsonResponse({'artists': list(artists)}, status=200)
    return render(request, 'onbeats/artists.html', {'artists': artists})


def get_search_result(request, query=None):
    if query:
        artists = Artist.objects.filter(name__contains=query)
        albums = Album.objects.filter(name__contains=query)
        songs = Song.objects.filter(name__contains=query)
        generated_html = render_to_string('onbeats/search-result-partial.html',
                                          context={'artists': artists,
                                                   'albums': albums,
                                                   'songs': songs
                                                   })
        return JsonResponse({"data": generated_html}, status=200)
    return render(request, 'onbeats/search-form.html')


def register(request):
    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.set_password(register_form.cleaned_data.get('password'))
            new_user.save()
            login(request, new_user)
            return redirect('onbeats:get_new_albums')
    else:
        register_form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'form': register_form})


def about_us(request):
    return render(request, 'onbeats/about-us.html', {})
