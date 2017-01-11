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
    "Unlimited-length CharField to satisfy Django `CharField` and postgreSQL `varchar` expectations."
    description = _("Unlimited-length string")

    def __init__(self, *args, **kwargs):
        """Like CharField constructor, but without max_length validation"""
        kwargs['max_length'] = int(1e9)  # Satisfy Django `manage.py validate`
        super(models.CharField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        """Return a string (type) representing the field data type

        'LongCharField' is unrecognized by Django as a valid field type
        So Django will raise an Exception if it looks for this string within its db_type() dict
        """
        return 'LongCharField'

    def db_type(self, connection):
        """A 'varchar' database field type without a max_length attribute

        In Postgres a 'varchar' with no max length is equivalent to 'text'
        But 'varchar' without max_length wont usually work in other DBs
        but 'varchar' used here so devs can tell LongCharFields from TextFields in psql
        """
        return 'varchar'

    def formfield(self, **kwargs):
        """Run parent CharField's formfield method without passing along a max_length."""
        return super(models.CharField, self).formfield(**kwargs)
models.LongCharField = LongCharField
