from django.conf.urls import patterns, include, url
import pacs.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hackor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', include(pacs)),
    url(r'^$', pacs.views.RawCommitteeTransactionsViewSet.as_view({'get':'list'})),
)
