
from django.conf.urls import include
from django.conf.urls import url
from django.apps import apps
from django.conf import settings
from django.contrib import admin
# from pacs.views import CommitteeTransactionsViewSet, RawCommitteeTransactionsViewSet
from rest_framework.routers import DefaultRouter

#from pacs import views
from guess import views as gviews
from predict_year import views as pviews

admin.autodiscover()

'''urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hackor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(pacs.urls)),
    # url(r'^$', pacs.views.RawCommitteeTransactionsViewSet.as_view({'get':'list'})),

)
'''

# Create a router and register our viewsets with it.
router = DefaultRouter()
# router.register(r'pacs', RawCommitteeTransactionsViewSet)
# router.register(r'bicycle', bviews.ListRacks)

for app_name in settings.APPS_TO_REST:
    app = apps.get_app_config(app_name)
    for lowercase_model_name, Model in app.models.iteritems():
        model_name = Model._meta.object_name
        viewset_class_name = model_name + 'ViewSet'
        router.register('hackor/' + app_name + '/' + model_name, getattr(views, viewset_class_name))


# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^uglyboxer/sketch/', gviews.parse_data, name='parse_data'),
    url(r'^uglyboxer/report/', gviews.show_data, name='show_data'),
    url(r'^uglyboxer/$', gviews.home_page, name='home'),
    url(r'^uglyboxer/validate/', gviews.valid_info, name='valid'),
    url(r'^uglyboxer/about/', gviews.about, name='about'),
    url(r'^uglyboxer/contact/', gviews.contact, name='contact'),
    url(r'^uglyboxer/stats/', gviews.stats_work, name='stats_work'),
    # url(r'^($|index.html$|/$)', 'django.contrib.staticfiles.views.serve', kwargs={
    #     'path': 'index.html', 'document_root': settings.STATIC_ROOT}),
    # url(r'^$', views.home_page, name='home'),
    url(r'^hackor/', include(router.urls)),  # for hackor and pacs API?
    # url(r'^$', include(router.urls)),
    url(r'^bicycle/', include('bicycle_theft.urls', namespace='bicycle_theft')),
    url(r'^year/', pviews.lyrics_prediction, name='predict_year'),
    url(r'^twote/', include('twote.urls', namespace='twote')),
]
