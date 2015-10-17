from django.core.management import BaseCommand
from pacs.models import RawCommitteeTransactions, CommitteeTransactions


def clean_duplicate_original_ids_from_raw_committee_transactions():
    """
        I'm wrapping this function in a manage command so it can be called in
    a migration and also be called by hand if data is ever manually updated.

        Also, this is absurdly slow (eta 20 min)...  Thanks django orm / me
    totally mis-using it.  The sql solution is
    http://stackoverflow.com/a/10999689/1224255 .
        Please drop that in instead of this loop via
    https://docs.djangoproject.com/en/1.8/ref/migration-operations/#runsql
    """

    CommitteeTransactions.objects.all().delete()

    last_oid = None
    # filter to [52810:52822] for a few good examples.  then uncomment print line
    # the `.iterator`
    for rct in RawCommitteeTransactions.objects.all().order_by('original_id', '-attest_date').iterator():
        # django throws in a `_state` key you need to ignore:

        original_id = rct.original_id
        # print original_id, rct.attest_date, '!' if last_oid == original_id else ' '
        if last_oid == original_id:
            pass
        else:
            CommitteeTransactions.objects.create(
                **{k: v for k, v in rct.__dict__.items() if k[0] != '_'})

        last_oid = original_id


class Command(BaseCommand):
    help = '''When transactions are modified, the original
    is kept and a new transaction is made (with a new transaction_id
    but the same original_id).  This copies the raw data into a
    cleaned table ignoring any transactions with a more current
    version.'''

    def handle(self, *args, **options):
        self.stdout.write("Aggregating stats on pre-de-dupe data...")
        full_amount_pre_de_dupe = sum(RawCommitteeTransactions.objects.values_list('amount', flat=True))
        n_pre_de_dupe = RawCommitteeTransactions.objects.count()

        self.stdout.write("Populating CommitteeTransaction table...")
        clean_duplicate_original_ids_from_raw_committee_transactions()

        self.stdout.write("Aggregating stats on cleaned data...")
        full_amount_post_de_dupe = sum(CommitteeTransactions.objects.values_list('amount', flat=True))
        n_post_de_dupe = CommitteeTransactions.objects.count()

        amount_of_lie = full_amount_pre_de_dupe - full_amount_post_de_dupe
        n_lies = n_pre_de_dupe - n_post_de_dupe

        print 'Dataset reduced by {} rows totaling an amount of {}$.'.format(n_lies, amount_of_lie)
