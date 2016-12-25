from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=100)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    def __str__(self):
        return "Event: {}".format(self.title)

class Room(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "Room: {}".format(self.name)


