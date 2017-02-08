from django.db import models
from django.core.validators import validate_comma_separated_integer_list
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
    guidebook_desc = models.TextField(default="", blank=True)
    online_desc = models.TextField(default="", blank=True)
    requirements = models.TextField(default="", blank=True)
    runners = models.TextField(default="", blank=True)
    badges = models.TextField(default="", validators=[validate_comma_separated_integer_list], blank=True)
    complete = models.BooleanField(default=False)
    public = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.title)

