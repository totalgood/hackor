from django.shortcuts import render
from hackor.pacs.models import RawCommitteeTransactions
from rest_framework import viewsets
from hackor.pacs.serializers import RawCommitteeTransactionsSerializer

class RawCommitteeTransactionsViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Raw Committee Transactions to be viewed."""
    queryset = RawCommitteeTransactions.objects.all
