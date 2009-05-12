from django.db import models
from django.contrib import admin

from constants import title_choices

class Person(models.Model):
    user = models.ForeignKey('auth.User', blank=True, null=True)
    groups = models.ManyToManyField('auth.Group', blank=True, null=True)
    title = models.CharField(max_length=4, choices=title_choices, blank=True, null=True)
    last = models.CharField(max_length=30)
    first = models.CharField(max_length=20)
    pic = models.ImageField(upload_to='our_people_avatars')
    description = models.TextField()
    email = models.EmailField()
    featured = models.BooleanField()

    def __unicode__(self):
        return "%s %s" % (self.first, self.last)

    def name(self):
        return self.__unicode__()

class PersonAdmin(admin.ModelAdmin):
    list_filter = ['groups', 'featured',]
    search_fields = ['last', 'first', 'description']
    list_display = ['__unicode__', 'user', 'featured']

admin.site.register(Person, PersonAdmin)
