from django.apps import apps
from django.conf import settings

from pacs.models import RawCommitteeTransactions, CommitteeTransactions
from rest_framework import serializers

from factory import create_class


for app_name in settings.APPS_TO_REST:
    app = apps.get_app_config('pacs')
    for lowercase_model_name, Model in app.models.iteritems():
        serializer_class_name = Model._meta.object_name + 'Serializer'
        if serializer_class_name not in globals():
            serializer_class = create_class(serializer_class_name, serializers.ModelSerializer)

        class Meta:
            model = Model

        serializer_class.Meta = Meta
        globals()[serializer_class_name] = serializer_class
