from django.urls import path
from . import views

app_name = 'onbeats'

urlpatterns = [
    path('', views.get_new_albums, name='get_new_albums'),
    path('artists/', views.get_all_artists, name='get_all_artists'),
    path('artist/<slug:artist_slug>/', views.get_artist, name='get_artist'),
    path('album/<slug:album_slug>/', views.get_album_songs,
         name='get_album_songs'),
    path('search/', views.get_search_result, name="search_page"),
    path('search/<str:query>/', views.get_search_result, name="search_result"),
    path('about-us/', views.about_us, name='about-us')
]
