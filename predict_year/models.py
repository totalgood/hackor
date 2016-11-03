from __future__ import unicode_literals

from django.db import models

class Song_BOW(models.Model):
    """How a song will be represented in BOW format in our DB"""

    bow = models.TextField(blank=True)
    year = models.IntegerField(default=None)
    confidence = models.FloatField(blank=True)
    prob_decades = models.TextField(blank=True)


