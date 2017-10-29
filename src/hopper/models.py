from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from django.conf import settings as d_settings
from django.dispatch import receiver
from datetime import datetime

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

class EventCommonInfo(models.Model):
    class Meta:
        abstract = True

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
    event_organiser = models.ForeignKey(d_settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    runners = models.CharField(max_length=300, default="", blank=True)
    badges = models.CharField(max_length=300, default="", validators=[validate_comma_separated_integer_list], blank=True)

class EventCompleted(EventCommonInfo):

    @classmethod
    def list_manual_concrete_fields(cls):
        fields = []
        for field in cls._meta.get_fields():
            if field.concrete and not field.auto_created and field.name != 'date_modified':
                fields.append(field)
        return fields

    @classmethod
    def write_from(cls, event):
        complete_kwargs = {}
        for field in cls.list_manual_concrete_fields():
            complete_kwargs[field.name] = getattr(event,field.name)
        if event.event_completed:
            complete_kwargs['pk']=event.event_completed_id
        complete = cls(**complete_kwargs)
        complete.save()
        return complete
            
    def compare(self, event):
        differences = set()
        for field in self.list_manual_concrete_fields():
            if getattr(self,field.name) != getattr(event,field.name):
                differences.add(field.name)
        return differences

    def __str__(self):
        return "{}".format(self.title)


class Event(EventCommonInfo):
    STATE_CHOICES = (
       ('D', 'DRAFT'),
       ('R', 'REVIEW'),
       ('C', 'COMPLETED'),
       ('A', 'AMENDED')
       )
    status = models.CharField(max_length=1, choices=STATE_CHOICES, default='D')
    public = models.BooleanField(default=False)
    event_completed = models.ForeignKey(EventCompleted, null=True, editable=False, on_delete=models.SET_NULL)
    date_modified = models.DateTimeField(auto_now=True)
    date_completed = models.DateTimeField(editable=False, null=True)

    __old_status = None

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self.__old_status = self.status

    def save(self, *args, **kwargs):
        if self.status == 'C':
            if self.__old_status != 'C':
                self.event_completed = EventCompleted.write_from(self)
                self.date_completed = datetime.now()
            else:
                if self.event_completed.compare(self):
                    self.status = 'A'
                    self.__old_status = self.status
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.title)

@receiver(models.signals.post_delete, sender=Event)
def delete_parent(sender, **kwargs):
    if kwargs['instance'].event_completed:
        kwargs['instance'].event_completed.delete()

