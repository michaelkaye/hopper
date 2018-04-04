from rest_framework import generics
from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from django.shortcuts import get_object_or_404

from hopper.models import Event, Room, EventCompleted
from hopper.serializers import EventSerializer, RoomSerializer
from hopper.permissions import EventAccessPermission

import logging

logger = logging.getLogger(__name__)

def health(request):
    return HttpResponse('')

def sched(request):
    template = loader.get_template('hopper/sched')
    if request.user.has_perm('hopper.download'):
        queryset = Event.objects.all()
        queryset = queryset.filter(status='C')
        queryset = queryset.filter(public=True)
        context = {
            'events': queryset
        }
        logger.info("Rendering queryset {}".format(queryset))
        return HttpResponse(template.render(context, request),
                content_type='text/csv')
    else:
        return None

def confirm_emails(request):
    template = loader.get_template('hopper/confirm_emails.html')
    if request.user.has_perm('hopper.download'):
        queryset = Event.objects.all()
        queryset = queryset.exclude(badges='')
        queryset = queryset.exclude(status='C')
        logger.info("Rendering queryset {}".format(queryset))
        events_set = list(queryset)
        for index, entry in enumerate(events_set):
            events_set[index].badges = entry.badges.split(',')
        context = {
            'events': events_set
        }
        return HttpResponse(template.render(context, request))
    else:
        return None

def compare_view(request, pk):
    _datetime_format = "%d %b, %A %H:%M"
    template = loader.get_template('hopper/compare.html')
    if request.user.is_authenticated:
        event = get_object_or_404(Event, pk=pk)
        event_completed = get_object_or_404(EventCompleted, pk=event.event_completed_id)
        diff = event_completed.compare(event)
        rows = []
        for field in EventCompleted.list_manual_concrete_fields():
            name = field.name
            try:
                event_val = getattr(event,field.name).strftime(_datetime_format)
            except AttributeError:
                event_val = getattr(event,field.name)
                completed_val = getattr(event_completed,field.name)
            else:
                completed_val = getattr(event_completed,field.name).strftime(_datetime_format)
            row = {'name' : name, 'event_val' : event_val, 'completed_val' : completed_val}
            if field.name in diff:
                row['is_diff'] = True
            rows.append(row)
        context = {'comparison': rows}
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseForbidden("Please log in via the admin page first")

def index(request):
    template = loader.get_template('hopper/index.html')
    if request.user.has_perm('hopper.add_event'): 
        editable='true'
    else:
        editable='false'
    context = {
        'defaultDate': '2018-05-26',
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

