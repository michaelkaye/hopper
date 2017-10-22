from rest_framework import generics
from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader

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

def compare_view(request, pk):
    template = loader.get_template('hopper/compare.html')
    if request.user.is_authenticated:
        event = Event.objects.get(pk=pk)
        event_completed = event.event_completed
        diff = event_completed.compare(event)
        rows = []
        for field in EventCompleted.list_manual_concrete_fields():
            row = {}
            row['name'] = field.name
            row['event_val'] = getattr(event,field.name)
            row['completed_val'] = getattr(event_completed,field.name)
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

