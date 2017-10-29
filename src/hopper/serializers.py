from rest_framework import serializers

from hopper.models import Event, Room

class EventSerializer(serializers.ModelSerializer):
    track = serializers.SlugRelatedField(
            read_only=True,
            slug_field='colour'
    )
    class Meta:
        model = Event
        fields = ("id", "title", "start", "end", "desc", "runners", "resourceId", "track")

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "title")

