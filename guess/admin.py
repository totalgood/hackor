from django.contrib import admin

# Register your models here.
from guess.models import Drawing, Stats


admin.site.register(Drawing)
admin.site.register(Stats)