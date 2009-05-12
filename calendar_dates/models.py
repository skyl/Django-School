from django.db import models
import settings

from djangogcal.adapter import CalendarAdapter, CalendarEvendata

class Date(models.Model):
    ''' For Gcalendar '''
    title = models.CharField(max_length=30)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __unicode__(self):
        return "%s - %s" % (self.title, self.start_time.date())

class DateCalendarAdapter(CalendarAdapter):

    def get_event_data(self, instance):
        return CalendarEventData(
                start=instance.start_time,
                end = instance.end_time,
                title=instance.title
                )
observer = CalendarObserver(email=settings.CALENDAR_EMAIL,
        password=settings.CALENDAR_PASSWORD)
observer.observe(Date, DateCalendarAdapter())
