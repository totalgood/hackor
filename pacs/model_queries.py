from models import RawCommitteeTransactions
from django.db.models import Sum


def top_filer_ids(sign=+1, n=500, table=RawCommitteeTransactions):
    """Compile sorted list of committees (filter IDs) by tranaction ammount

    Args:
      sign (int):  Determines subset of transactions summed
        positive = +1, negative = -1, or net = 0
      n (int): Maximum number of filer_ids to return
      table (Model): model to query (must have 'amount' and 'filer_id' fields)
    """
    qs = table.objects
    if sign > 0:
        qs = qs.filter(amount__gt=0)
    if sign < 0:
        qs = qs.filter(amount__lt=0)
    return qs.values('filer_id').annotate(total=Sum('amount')).order_by('-total').values()[:n]
