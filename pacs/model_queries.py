from model_utils import models
from pacs.models import RawCommitteeTransactions
from django.db.models import Sum


def top_filer_ids(sign=+1, n=500, start_date='2014-01-01', end_date='2015-12-31', date_field='filed_date',
                  table=RawCommitteeTransactions):
    """Compile sorted list of committees (filter IDs) by tranaction ammount

    Args:
      sign (int):  Determines subset of transactions summed
        positive = +1, negative = -1, or net = 0
      n (int): Maximum number of filer_ids to return
      table (Model): model to query (must have 'amount', 'filer_id', and 'tran_date' fields)

    $ python manage.py shell
    >>> for f in top_filer_ids(sign=+1, n=10, start_date='2014-01-01', end_date='2015-12-31'):
    ...     print(f['filer_id'], f['filer'], f['total'])
    (17015, u'NO on 92 Coalition', 4460000.0)
    (16171, u'New Approach Oregon', 2267863.02)
    (17001, u'Vote Yes on 90', 1250000.0)
    (13920, u'Kitzhaber for Governor', 1131461.35)
    (17007, u'Vote Yes on Measure 92: We have the right to know whats in our food', 1099999.88)
    (17155, u'Open Primaries', 1000000.0)
    (17044, u'Yes on 91', 877809.0)
    (5486, u'American Federation of Teachers-Oregon Issue PAC', 592753.65)
    (16651, u'Oregonians for Competition 7', 500000.0)
    (13130, u'Defend Oregon', 500000.0)
    """
    if date_field not in set(f.name for f in table._meta.fields):
        date_field = None
    date_field = date_field or (f for f in table._meta.fields
                                if isinstance(f, (models.DateTimeField, models.DateField))).next()
    if not isinstance(date_field, basestring):
        date_field = date_field.name
    qs = table.objects
    if sign > 0:
        qs = qs.filter(amount__gt=0)
    if sign < 0:
        qs = qs.filter(amount__lt=0)
    if start_date:
        kwargs = {date_field + '__gte': start_date}
        qs = qs.filter(**kwargs)
    if end_date:
        kwargs = {date_field + '__lte': end_date}
        qs = qs.filter(**kwargs)
    qs = qs.values('filer_id').annotate(total=Sum('amount')).order_by('-total').values()
    # hack to acomplish distinct('filer_id') queryset filter
    filers = []
    filer_ids = set()
    for rec in qs:
        if rec['filer_id'] not in filer_ids:
            filers += [rec]
            filer_ids.add(rec['filer_id'])
        if len(filers) >= n:
            return filers
    return filers
