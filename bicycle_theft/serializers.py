from . import models 
from rest_framework_gis import serializers as gis_serializer 


class BikeParkingSerializer(gis_serializer.GeoModelSerializer):

    class Meta:
        fields = (
            'id',
            #'longitude',
            #'latitude',
            'geom',
            'theft_prob_per_bike_day_x_1000',
            )
        model = models.BicycleParkingPdx
        geo_field = 'geom'

