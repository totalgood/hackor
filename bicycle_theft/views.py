from rest_framework_gis.filters import DistanceToPointFilter
from rest_framework_gis.pagination import GeoJsonPagination
from rest_framework import generics

from . import models
from . import serializers 

class ListRacks(generics.ListAPIView):
    """
    This endpoint lists all racks in the database with their ids, geom points (long-lat coords),
    and theft score. 

    To search for racks within given distance you must pass in a query string 
    with a distance in which you want to search and a point which is a set of coordinates
    in lon,lat format.

    eg: totalgood.org/bicycle/?dist=50&point=-122.678713,45.514798

    Which is equivalant to filtering within 50 meters of the point (-122.678713,45.514798). 

    """
    queryset = models.BicycleParkingPdx.objects.all()
    serializer_class = serializers.BikeParkingSerializer
    distance_filter_field = 'geom'
    filter_backends = (DistanceToPointFilter, )
    distance_filter_convert_meters = True

    




