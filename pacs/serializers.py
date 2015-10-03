

from pacs.models import RawCommitteeTransactions
from rest_framework import serializers


class RawCommitteeTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawCommitteeTransactions
        
