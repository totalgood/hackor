from django.apps import apps
from rest_framework import viewsets
from rest_framework import filters
from django.conf import settings

from pacs.factory import create_class
import pacs.serializers

unfilterable_field_types = ('OneToOneField', 'ForeignKey', 'ManyToManyField')


for app_name in settings.APPS_TO_REST:
    app = apps.get_app_config('pacs')
    for model_name, Model in app.models.iteritems():
        viewset_class_name = model_name + 'ViewSet'
        if viewset_class_name not in globals():
            viewset_class = create_class(viewset_class_name, viewsets.ReadOnlyModelViewSet)
        viewset_class.serializer_class = pacs.serializers.get(model_name + 'Serializer')
        viewset_class.filter_backends = (filters.DjangoFilterBackend,)
        viewset_class.filter_fields = tuple([field.name for field in Model._meta.fields
                                            if not field.get_internal_type() in unfilterable_field_types])
        viewset_class.filter_fields = tuple(['categoria', 'categoria__titulo'])
        globals()[viewset_class_name] = viewset_class
