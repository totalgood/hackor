from django.conf.urls import patterns, include, url
import pacs.urls
from pacs import views
from django.contrib import admin

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
urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
    url(r'^pacs/$', views.RawCommitteeTransactions_list),
]
