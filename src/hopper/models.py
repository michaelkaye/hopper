from django.db import models

class Room(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return "Room: {}".format(self.title)

def get_default_room():
    return Room.objects.get_or_create(title="Nowhere")[0]

class Event(models.Model):
    title = models.CharField(max_length=100)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    resourceId = models.ForeignKey(
        Room,
        on_delete=models.SET(get_default_room)
    );
    def __str__(self):
        return "Event: {}".format(self.title)




