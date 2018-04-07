from datetime import datetime, tzinfo, timedelta
from rest_framework import generics
from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from django.shortcuts import get_object_or_404
from xml.sax.saxutils import escape
from hopper.models import Event, Room, EventCompleted
from hopper.serializers import EventSerializer, RoomSerializer
from hopper.settings import HOPPER_PASSWORD
from hopper.permissions import EventAccessPermission

import logging
import pytz

logger = logging.getLogger(__name__)

def health(request):
    return HttpResponse('')

ZERO = timedelta(0)
class UTC(tzinfo):
    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO
utc = UTC()
london = pytz.timezone("Europe/London");

def xml(request):
    queryset = Event.objects.all()
    queryset = queryset.exclude(track__title='UNAVAILABLE').exclude(track__title='Internal')
    queryset = queryset.order_by('start');
    logger.info("Rendering queryset {}".format(queryset))
    # annoyingly we can't do it with a template.
    string = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><events><days>'
    friday_am = datetime(2018, 05, 25, 6, 0, 0, tzinfo=utc)
    saturday_am = datetime(2018, 05, 26, 6, 0, 0, tzinfo=utc)
    sunday_am = datetime(2018, 05, 27, 6, 0, 0, tzinfo=utc)
    monday_am = datetime(2018, 05, 28, 6, 0, 0, tzinfo=utc)
    tuesday_am = datetime(2018, 05, 29, 6, 0, 0, tzinfo=utc)
    wednesday_am = datetime(2018, 05, 30, 6, 0, 0, tzinfo=utc)
    events = [event for event in queryset if event.end]
    friday = [event for event in events if event.start > friday_am and event.end < saturday_am]
    saturday = [event for event in events if event.start > saturday_am and event.end < sunday_am]
    sunday = [event for event in events if event.start > sunday_am and event.end < monday_am]
    monday = [event for event in events if event.start > monday_am and event.end < tuesday_am]
    tuesday = [event for event in events if event.start > tuesday_am and event.end < wednesday_am]
    days = [friday, saturday, sunday, monday, tuesday]
    for x in range(0,len(days)):
        string = string + "<day-{}>".format(x)
        for event in days[x]:
            string = string + _eventfragment(event)
        string = string + '</day-{}>'.format(x)
    string = string + '</days></events>'
    return HttpResponse(string, content_type='text/plain')
def _eventfragment(event):
    title = escape(event.title)
    if ('---' in event.desc) {
        parts = event.desc.split('---',2);
        abstract = '<abstract>'+escape(parts[0])+'</abstract>\u2029<nonsense>'+escape(parts[1])+'</nonsense>';
    } else {
        abstract = '<abstract>'+escape(event.desc)+'</abstract>';
    }
    persons = escape(event.runners)
    start = event.start.astimezone(london).strftime("%a at %H:%M")
    end = event.end.astimezone(london).strftime("%H:%M")
    time = "{} to {}".format(start, end)
    room = escape(event.resourceId.title)
    try:
        return u"<event><title>{}</title>\u2029<timedate>{}</timedate>\u2029{}\u2029<persons>{}</persons>\u2029<room>{}</room>\u2029</event>".format(title, time, abstract, persons, room)
    except UnicodeEncodeError:
        logger.error(event);
        return "<event><!-- Event {} failed to encode --></event>".format(event.pk);
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

