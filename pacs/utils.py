from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _


def representation(model, field_names=[]):
    """Unicode representation of Django model instance (object/record/row)"""
    if not field_names:
        field_names = getattr(model, 'IMPORTANT_FIELDS', ['pk'])
    retval = model.__class__.__name__ + u'('
    retval += ', '.join("%s" % (repr(getattr(model, s, '') or ''))
                        for s in field_names[:min(len(field_names), representation.max_fields)])
    return retval + u')'
representation.max_fields = 5


def name_similarity():
    """Compute the similarity (inverse distance) matrix between committe names"""
    pass


class LongCharField(models.CharField):
    "An unlimited-length CharField to satisfy by Django and postgreSQL varchar."
    description = _("Unlimited-length string")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = int(1e9)  # Satisfy management validation.
        super(models.CharField, self).__init__(*args, **kwargs)
        # Don't add max-length validator like CharField does.

    def get_internal_type(self):
        # This has no function, since this value is used as a lookup in
        # db_type().  Put something that isn't known by django so it
        # raises an error if it is ever used.
        return 'LongCharField'

    def db_type(self, connection):
        # *** This is probably only compatible with Postgres.
        # 'varchar' with no max length is equivalent to 'text' in Postgres,
        # but put 'varchar' so we can tell LongCharFields from TextFields
        # when we're looking at the db.
        return 'varchar'

    def formfield(self, **kwargs):
        # Don't pass max_length to form field like CharField does.
        return super(models.CharField, self).formfield(**kwargs)
models.LongCharField = LongCharField


