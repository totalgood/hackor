from model_utils import models
from pacs.models import RawCommitteeTransactions
from django.db.models import Sum


def top_filer_ids(sign=+1, n=500, start_date=None, end_date=None, date_field=None, table=RawCommitteeTransactions):
    """Compile sorted list of committees (filter IDs) by tranaction ammount

    Args:
      sign (int):  Determines subset of transactions summed
        positive = +1, negative = -1, or net = 0
      n (int): Maximum number of filer_ids to return
      table (Model): model to query (must have 'amount', 'filer_id', and 'tran_date' fields)
    """
    date_field = date_field or (f for f in table.fields
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
    return qs.values('filer_id').annotate(total=Sum('amount')).order_by('-total').values()[:n]
