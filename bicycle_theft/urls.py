from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.ListRacks.as_view(), name='rack_list'),
    url(r'^sorted/$', views.ClosestDist.as_view(), name='sorted_racks')
]



