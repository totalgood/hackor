

from pacs.models import RawCommitteeTransactions, CommitteeTransactions
from rest_framework import serializers


class RawCommitteeTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawCommitteeTransactions


class CommitteeTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitteeTransactions
