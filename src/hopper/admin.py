from django.contrib import admin
from hopper.models import Event, Room, Track
from django.forms import TextInput, Textarea
from django.db import models

class EventAdmin(admin.ModelAdmin):
    fieldsets = (
            (None, {
                'fields': ('title', 'track', 'runners', 'badges', 'online_desc', 'guidebook_desc', 'requirements', 'complete', 'public')
            }),
            ('Time and Room', {
                'classes': ('collapse',),
                'fields': ('start', 'end', 'resourceId')
            })
        )
    list_filter = ('track', 'resourceId', 'public', 'complete')
    search_fields = ['title', 'runners', 'track__title', 'resourceId__title']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':40})},
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols':40})}
    }

admin.site.register(Track)
admin.site.register(Event, EventAdmin)
admin.site.register(Room)
