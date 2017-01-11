from bicycle_theft import models as theft_models 
from django.contrib import admin
from django.db.models.base import ModelBase

# Register your models here.

for name, var in theft_models.__dict__.items():
    if type(var) is ModelBase:
        admin.site.register(var)
