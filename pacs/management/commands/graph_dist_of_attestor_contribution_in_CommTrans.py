from django.core.management import BaseCommand
from django.db.models import Count
from pacs.models import RawCommitteeTransactions


class Command(BaseCommand):

    help = ''' For curiosity, plotting the histogram
    of the number of attests for each attest_by_name
    in RawCommitteeTransactions.'''

    def handle(self, *args, **options):
        try:
            from matplotlib import pylab as pl
            import numpy as np
        except ImportError:
            raise Exception('Be sure to install requirements_scipy.txt before running this.')

        all_names_and_counts = RawCommitteeTransactions.objects.all().values('attest_by_name').annotate(total=Count('attest_by_name')).order_by('-total')
        all_names_and_counts_as_tuple_and_sorted = sorted([(row['attest_by_name'], row['total']) for row in all_names_and_counts], key=lambda row: row[1])
        print "top ten attestors:  (name, number of transactions they attest for)"
        for row in all_names_and_counts_as_tuple_and_sorted[-10:]:
            print row

        n_bins = 100
        filename = 'attestor_participation_distribution.png'

        x_max = all_names_and_counts_as_tuple_and_sorted[-31][1]  # eliminate top outliers from hist
        x_min = all_names_and_counts_as_tuple_and_sorted[0][1]

        counts = [row['total'] for row in all_names_and_counts]
        pl.figure(1, figsize=(18, 6))
        pl.hist(counts, bins=np.arange(x_min, x_max, (float(x_max)-x_min)/100) )
        pl.title('Histogram of Attestor Participation in RawCommitteeTransactions')
        pl.xlabel('Number of transactions a person attested for')
        pl.ylabel('Number of people')
        pl.savefig(filename)