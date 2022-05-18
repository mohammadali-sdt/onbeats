import random
from datetime import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator, MaxValueValidator, \
    FileExtensionValidator
from gdstorage.storage import GoogleDriveStorage


gd_storage = GoogleDriveStorage()

# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    profile = models.ImageField(max_length=5000, upload_to='artists_profile/',
                                blank=False, null=False, storage=gd_storage)
    cover = models.ImageField(max_length=5000, upload_to='artists_cover/',
                              blank=False, null=False, storage=gd_storage)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Artist, self).save(*args, **kwargs)


class Style(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE,
                               related_name='styles')

    def __str__(self):
        return f'{self.name}-{self.artist.name}'

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Style, self).save(*args, **kwargs)


class Album(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE,
                               related_name='albums')
    genre = models.CharField(max_length=255, blank=False,
                             null=False)  # must be Choice Field
    release_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900),
                    MaxValueValidator(datetime.now().year)],
        help_text='Use the following format: YYYY', blank=False, null=False)
    cover = models.ImageField(max_length=5000, upload_to='albums_cover/',
                              blank=False, null=False, storage=gd_storage)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True)

    # num_of_tracks
    def _get_num_of_tracks(self):
        return self.songs.count()

    number_of_tracks = property(_get_num_of_tracks)

    def __str__(self):
        return f'{self.name}-{self.artist.name}'

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.genre = self.genre.lower()
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Album, self).save(*args, **kwargs)


class Song(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE,
                              related_name='songs')
    file = models.FileField(upload_to='songs_file/', blank=False, null=False,
                            validators=[FileExtensionValidator(
                                allowed_extensions=['mp3'])],
                            help_text='Allowed .mp3 files', storage=gd_storage)

    # file_ogg = models.CharField(blank=True, editable=False, max_length=50000)
    track_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], blank=False, null=False)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()

        # conversion mp3 file
        # self.file.read()
        # self.file.name = self.file.name.replace(' ', '-')
        # print(self.file.name)
        return super(Song, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}-{self.album.name}'
