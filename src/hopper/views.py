from rest_framework import generics
from django.http import HttpResponse
from django.template import loader

from hopper.models import Event, Room
from hopper.serializers import EventSerializer, RoomSerializer
from hopper.settings import PASSWORD
from hopper.permissions import EventAccessPermission

import logging

logger = logging.getLogger(__name__)

def health(request):
    return HttpResponse('')

def xml(request):
    if request.GET['password'] == PASSWORD:
        queryset = Event.objects.all()
        queryset = queryset.filter(complete=True)
        logger.info("Rendering queryset {}".format(queryset))
        # annoyingly we can't do it with a template.
        string = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><events><days><day-1>'
        for event in queryset:
            string = string + _eventfragment(event)
        string = string + '</day-1></days></events>'
        return HttpResponse(string, content_type='text/plain')
    else:
        return None
def _eventfragment(event):
    title = event.title
    abstract = event.guidebook_desc
    persons = event.runners
    start = event.start.strftime("%a at %H:%M")
    end = event.end.strftime("%H:%M")
    time = "{} to {}".format(start, end)
    room = event.resourceId.title
    return "<event><title>{}</title><timedate>{}</timedate><abstract>{}</abstract><persons>{}</persons><room>{}</room></event>".format(title, time, abstract, persons, room)

def sched(request):
    template = loader.get_template('hopper/sched')
    if request.user.is_authenticated:
        queryset = Event.objects.all()
        queryset = queryset.filter(complete=True)
        queryset = queryset.filter(public=True)
        context = {
            'events': queryset
        }
        logger.info("Rendering queryset {}".format(queryset))
        return HttpResponse(template.render(context, request),
                content_type='application/xml')
    else:
        return None

def index(request):
    template = loader.get_template('hopper/index.html')
    logger.info(request.user.is_authenticated)
    if request.user.is_authenticated and request.user.has_perm('hopper.add_event'): 
        editable='true'
    else:
        editable='false'
    context = {
        'defaultDate': '2017-05-27',
        'editable': editable
    }
    return HttpResponse(template.render(context, request))


class EventList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Event.objects.all()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(public=True)
        has_time = self.request.query_params.get('has_time', False)
        if has_time is not None:
            if 'true' == has_time:
                queryset = queryset.exclude(start__isnull=True)
            else:
                queryset = queryset.filter(start__isnull=True)
        return queryset

    serializer_class = EventSerializer

class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = (EventAccessPermission, )
    def get_queryset(self):
        queryset = Event.objects.all()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(public=True)
        return queryset

class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

