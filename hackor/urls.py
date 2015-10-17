from django.conf.urls import include, url
from django.contrib import admin
from pacs.views import CommitteeTransactionsViewSet, RawCommitteeTransactionsViewSet
from rest_framework.routers import DefaultRouter

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
router.register(r'pacs', RawCommitteeTransactionsViewSet)
router.register(r'pac_transactions', CommitteeTransactionsViewSet)

# The API URLs are now determined automatically by the router.

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
]

