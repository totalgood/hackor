
from rest_framework import viewsets

from pacs.models import RawCommitteeTransactions, CommitteeTransactions
from pacs.serializers import RawCommitteeTransactionsSerializer, CommitteeTransactionsSerializer


class RawCommitteeTransactionsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides 'list' and 'detail' actions.
    """
    queryset = RawCommitteeTransactions.objects.all()
    serializer_class = RawCommitteeTransactionsSerializer

class CommitteeTransactionsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides 'list' and 'detail' actions.
    """
    queryset = CommitteeTransactions.objects.all()
    serializer_class = CommitteeTransactionsSerializer

        




