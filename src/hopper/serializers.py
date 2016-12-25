from rest_framework import serializers

from hopper.models import Event, Room

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("id", "title", "start", "end", "resourceId")

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "title")

