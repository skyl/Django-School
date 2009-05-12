from django.db import models
from django.db.models import permalink
from django.conf import settings
from tagging.fields import TagField

import tagging

from django.contrib.auth.models import User

class AudioSet(models.Model):
  """ AudioSet model """ 
  # here is where we link to the users
  users         = models.ManyToManyField(User)

  title         = models.CharField(max_length=255)
  slug          = models.SlugField(unique=True)
  description   = models.TextField(blank=True)
  audios        = models.ManyToManyField('Audio', related_name='audio_sets')
  created       = models.DateTimeField(auto_now_add=True)
  modified      = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'media_audio_sets'

  class Admin:
    pass

  def __unicode__(self):
    return '%s' % self.title

  @permalink
  def get_absolute_url(self):
      return ('audio_set_detail', None, { 'user':self.user.username,'slug': self.slug })


class Audio(models.Model):
  """ Audio model """
  user         = models.ForeignKey(User)
  title         = models.CharField(max_length=255)
  slug          = models.SlugField(unique=True)
  still         = models.FileField(upload_to='audio_stills', blank=True, help_text='An image that will be used as a thumbnail.')
  #audio         = models.FilePathField(path=settings.MEDIA_ROOT+'audios/', recursive=True)
  audio         = models.FileField(upload_to='audios')
  description   = models.TextField(blank=True)
  tags          = TagField()
  uploaded      = models.DateTimeField(auto_now_add=True)
  modified      = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'media_audio'
    verbose_name_plural = 'audios'

  class Admin:
    pass

  def __unicode__(self):
    return '%s' % self.title

  @permalink
  def get_absolute_url(self):
      return ('audio_detail', None, { 'user':self.user.username, 'slug': self.slug })


class PhotoSet(models.Model):
  """ PhotoSet model """
  users         = models.ManyToManyField(User)
  title         = models.CharField(max_length=255)
  slug          = models.SlugField(unique=True)
  description   = models.TextField(blank=True)
  cover_photo   = models.ForeignKey('Photo', blank=True, null=True)
  photos        = models.ManyToManyField('Photo', related_name='photo_sets')
  created       = models.DateTimeField(auto_now_add=True)
  modified      = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'media_photo_sets'

  class Admin:
    pass

  def __unicode__(self):
    return '%s' % self.title

  @permalink
  def get_absolute_url(self):
    return ('photo_set_detail', None, { 'slug': self.slug })


class Photo(models.Model):
  """ Photo model """
  user          = models.ForeignKey(User)
  LICENSES = (
      ('http://creativecommons.org/licenses/by/2.0/',         'CC Attribution'),
      ('http://creativecommons.org/licenses/by-nd/2.0/',      'CC Attribution-NoDerivs'),
      ('http://creativecommons.org/licenses/by-nc-nd/2.0/',   'CC Attribution-NonCommercial-NoDerivs'),
      ('http://creativecommons.org/licenses/by-nc/2.0/',      'CC Attribution-NonCommercial'),
      ('http://creativecommons.org/licenses/by-nc-sa/2.0/',   'CC Attribution-NonCommercial-ShareAlike'),
      ('http://creativecommons.org/licenses/by-sa/2.0/',      'CC Attribution-ShareAlike'),
  )
  title         = models.CharField(max_length=255)
  slug          = models.SlugField(unique=True)
  photo         = models.FileField(upload_to="photos")
  taken_by      = models.CharField(max_length=100, blank=True)
  license       = models.URLField(blank=True, choices=LICENSES)
  description   = models.TextField(blank=True)
  tags          = TagField()
  uploaded      = models.DateTimeField(auto_now_add=True)
  modified      = models.DateTimeField(auto_now=True)
  _exif         = models.TextField(blank=True)
  def _set_exif(self, d):
      self._exif = simplejson.dumps(d)
  def _get_exif(self):
      if self._exif:
          return simplejson.loads(self._exif)
      else:
          return {}
  exif = property(_get_exif, _set_exif, "Photo EXIF data, as a dict.")

  class Meta:
    db_table = 'media_photos'

  class Admin:
    pass

  def __unicode__(self):
    return '%s' % self.title
  
  @property
  def url(self):
    return '%s%s' % (settings.MEDIA_URL, self.photo)
  
  @permalink
  def get_absolute_url(self):
      return ('photo_detail', None, { 'user':self.user.username, 'slug': self.slug })


class VideoSet(models.Model):
  """ VideoSet model """
  group         = models.ForeignKey('Group', blank=True)
  title         = models.CharField(max_length=255)
  slug          = models.SlugField(unique=True)
  description   = models.TextField(blank=True)
  videos        = models.ManyToManyField('Video', related_name='video_sets')
  created       = models.DateTimeField(auto_now_add=True)
  modified      = models.DateTimeField(auto_now=True)
  
  class Meta:
    db_table = 'media_video_sets'
  
  class Admin:
    pass
  
  def __unicode__(self):
    return '%s' % self.title

  @permalink
  def get_absolute_url(self):
    return ('video_set_detail', None, { 'slug': self.slug })


class Video(models.Model):
  """ Video model """ 
  user          = models.ForeignKey(User)
  title         = models.CharField(max_length=255)
  slug          = models.SlugField(unique=True)
  still         = models.FileField(upload_to='video_stills',\
          blank=True, help_text='An image that will be used as a thumbnail.')
  # Video field should be an uplaod field.
  #video         = models.FilePathField(path=settings.MEDIA_ROOT+'videos/', recursive=True)
  video         = models.FileField(upload_to='videos',\
          help_text='upload a video in flv format')
  description   = models.TextField(blank=True)
  tags          = TagField()
  uploaded      = models.DateTimeField(auto_now_add=True)
  modified      = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'media_videos'

  class Admin:
    pass

  def __unicode__(self):
    return '%s' % self.title

  @permalink
  def get_absolute_url(self):
      return ('video_detail', None, {'slug': self.slug, })

class Group(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    members = models.ManyToManyField(User)
    pic = models.FileField(upload_to='group_pics')

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return ('group_detail', None, { 'slug':self.slug })
