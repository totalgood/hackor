from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.shortcuts import render
from pacs.models import RawCommitteeTransactions
from rest_framework import viewsets
from pacs.serializers import RawCommitteeTransactionsSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

'''
class RawCommitteeTransactionsViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Raw Committee Transactions to be viewed."""
    queryset = RawCommitteeTransactions.objects.all
'''

def RawCommitteeTransactions_list(request):
    """
    List all RawCommitteeTransactions fields
    """
    if request.method == 'GET':
        rtc = RawCommitteeTransactions.objects.all()[:100]
        serializer = RawCommitteeTransactionsSerializer(rtc, many=True)
        return JSONResponse(serializer.data)


