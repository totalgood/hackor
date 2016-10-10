from django.contrib.gis.db import models

srid = 4326

class BicycleParkingPdx(models.Model):
    id = models.AutoField(primary_key=True)
    #longitude = models.FloatField(blank=True, null=True)
    #latitude = models.FloatField(blank=True, null=True)
    geom = models.GeometryField(srid=srid)
    theft_prob_per_bike_day_x_1000 = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True)
    objects = models.GeoManager() 

    class Meta:
        managed = True
        db_table = 'bicycle_parking_pdx'

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

