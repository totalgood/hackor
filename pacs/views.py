
from rest_framework import viewsets

from pacs.models import RawCommitteeTransactions
from pacs.serializers import RawCommitteeTransactionsSerializer


class RawCommitteeTransactionsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides 'list' and 'detail' actions.
    """
    queryset = RawCommitteeTransactions.objects.all()
    serializer_class = RawCommitteeTransactionsSerializer


        




