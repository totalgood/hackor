from rest_framework_gis.filters import DistanceToPointFilter
from rest_framework_gis.pagination import GeoJsonPagination
from rest_framework import generics

from django.contrib.gis.geos import Point

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

# --------------------------------------------------------------------------------------

class ClosestDist(generics.ListAPIView):
    """Endpoint takes number of racks lat/long coords and returns a sorted list
        of racks by distance equal to the number provied.

        Ex. http://localhost:8000/api/v1/racks/sorted/?racks=50&point=-122.678713,45.514798
        will return 50 racks sorted by distance of the lat/lng point provied"""

    serializer_class = serializers.BikeParkingSerializer


    def get_queryset(self):
        """get lat/lng point object and number of racks and return num of sorted racks by closest dist"""

        radial_dist = .01
        point = self.get_filter_point(self.request)
        num_racks = self.request.query_params.get('racks', 30)

        bike_racks = self.distance_orderer(num_racks, radial_dist, point)

        # if nothing returned increase search distance before returning results
        while len(bike_racks) <= 25:
            radial_dist += .1
            bike_racks = self.distance_orderer(num_racks, radial_dist, point)

        return bike_racks

    def get_filter_point(self, request):
        """grab point out of query string and make a geos point"""

        point_string = request.query_params.get('point', None)

        if not point_string:
            return None
        try:
            (x, y) = (float(n) for n in point_string.split(','))
        except ValueError:
            raise ParseError('Invalid geometry string supplied for parameter {0}'.format(self.point_param))

        point_string = Point(x, y, 4326)

        return point_string

    def distance_orderer(self, num_racks, radial_dist, point):
        """helper method to adjust search distance incase no results returned on first try"""

        bike_racks = models.BicycleParkingPdx.objects.filter(geom__dwithin=(point, radial_dist)).distance(point).order_by('distance')[:num_racks]

        return bike_racks




