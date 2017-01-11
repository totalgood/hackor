from rest_framework import serializers
from models import Song_BOW


class BOWSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song_BOW
        fields = ('bow', 'year', 'confidence', 'prob_decades')