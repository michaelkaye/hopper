from django.contrib import admin
from hopper.models import Event, Room, Track
from django.forms import TextInput, Textarea
from django.db import models

class EventAdmin(admin.ModelAdmin):
    fieldsets = (
            (None, {
                'fields': ('title', 'track', 'event_organiser', 'runners', 'badges', 'desc', 'requirements', 'internal', ('status', 'public'))
            }),
            ('Time and Room', {
                'fields': ('start', 'end', 'resourceId')
            })
        )
    list_display = ('title', 'date_modified', 'date_completed')
    list_filter = ('track', 'resourceId', 'status', 'public')
    search_fields = ['title', 'runners', 'track__title', 'resourceId__title']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':60})},
        models.TextField: {'widget': Textarea(attrs={'rows': 5, 'cols':60})}
    }

admin.site.register(Track)
admin.site.register(Event, EventAdmin)
admin.site.register(Room)
