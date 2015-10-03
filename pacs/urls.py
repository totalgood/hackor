from django.conf.urls import url
from pacs import views

urlpatterns = [
        url(r'pacs/$', views.RawCommitteeTransactions_list),
        ]
