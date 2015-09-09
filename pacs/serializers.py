

from pacs.models import RawCommitteeTransactions
from rest_framework import serializers


class RawCommitteeTransactionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RawCommitteeTransactions
        fields = ('tran_id', )
