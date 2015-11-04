from django.conf.urls import include
from django.conf.urls import url
from django.apps import apps
from django.conf import settings
from django.contrib import admin
# from pacs.views import CommitteeTransactionsViewSet, RawCommitteeTransactionsViewSet
from rest_framework.routers import DefaultRouter

from pacs import views
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


for app_name in settings.APPS_TO_REST:
    app = apps.get_app_config(app_name)
    for lowercase_model_name, Model in app.models.iteritems():
        model_name = Model._meta.object_name
        viewset_class_name = model_name + 'ViewSet'
        router.register(app_name + '/' + model_name, getattr(views, viewset_class_name))


# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
]
