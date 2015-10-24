from django.apps import apps
from rest_framework import viewsets
from rest_framework import filters
from django.conf import settings

from pacs.factory import create_class
import pacs.serializers

unfilterable_field_types = set(['OneToOneField', 'ForeignKey', 'ManyToManyField', 'AutoField'])
unfilterable_field_names = set(['id', 'pk', 'primary_key'])


print('Creating REST interface for...')
for app_name in settings.APPS_TO_REST:
    app = apps.get_app_config(app_name)
    print('App: {}'.format(app_name))
    for lowercase_model_name, Model in app.models.iteritems():
        model_name = Model._meta.object_name
        print('    Model: {}'.format(model_name))
        viewset_class_name = model_name + 'ViewSet'
        if viewset_class_name not in globals():
            viewset_class = create_class(viewset_class_name, viewsets.ReadOnlyModelViewSet)
        viewset_class.filter_fields = tuple(field.name for field in Model._meta.fields
                                            if not field.get_internal_type() in unfilterable_field_types
                                            and not field.primary_key
                                            and not field.name in unfilterable_field_names)
        viewset_class.serializer_class = getattr(pacs.serializers, model_name + 'Serializer')
        viewset_class.filter_backends = (filters.DjangoFilterBackend,)
        viewset_class.queryset = Model.objects.all()
        globals()[viewset_class_name] = viewset_class
