from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from django.conf import settings as d_settings



class Room(models.Model):
    title = models.CharField(max_length=100)
    size = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.title)

class Track(models.Model):
    title = models.CharField(max_length=40)
    colour = models.CharField(max_length=40)
    def __str__(self):
        return "{}".format(self.title)

class Event(models.Model):
    STATE_CHOICES = (
       ('D', 'DRAFT'),
       ('R', 'REVIEW'),
       ('C', 'COMPLETED'),
       ('A', 'AMENDED')
       )
    title = models.CharField(max_length=100)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    track = models.ForeignKey(
        Track,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    );
    resourceId = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    );
    runners = models.CharField(max_length=300, null=True, blank=True)
    desc = models.TextField(default="", blank=True)
    requirements = models.TextField(default="", blank=True)
    internal = models.TextField(default="", blank=True)
    status = models.CharField(max_length=1, choices=STATE_CHOICES, default='D')
    event_organiser = models.ForeignKey(d_settings.AUTH_USER_MODEL)
    last_modified = models.DateTimeField(auto_now=True)
    last_confirmed = models.DateTimeField(null=True, blank=True, editable=False)
    runners = models.CharField(max_length=300, default="", blank=True)
    badges = models.CharField(max_length=300, default="", validators=[validate_comma_separated_integer_list], blank=True)
    public = models.BooleanField(default=False)

    __old_status = None

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self.__old_status = self.status

    def save(self, *args, **kwargs):
        if self.__old_status == 'C':
            self.status = 'A'
        super(Event, self).save(*args, **kwargs)
        self.__old_status = self.status


    def __str__(self):
        return "{}".format(self.title)

