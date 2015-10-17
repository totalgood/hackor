from django.test import TestCase

#TODO:  Turns out tests fail with how the first migration is set up.
# Looks like the expectation of having manually imported the database
# dump and the tests not having a way to do that causes the test
# infrastructure to blow up.  Leaving this file / comment here as a
# reminder to clean up the database creation / initial import to work
# with this test framework.
from pacs.management.commands.clean_committee_transactions import \
    clean_duplicate_original_ids_from_raw_committee_transactions
from pacs.models import RawCommitteeTransactions, CommitteeTransactions


class TestDataCleaning(TestCase):
    def test_de_duping_of_committee_transaction_based_on_original_id(self):
        # Set up a few rows of known data
        # RawCommitteeTransactions.objects.create(...)
        clean_duplicate_original_ids_from_raw_committee_transactions()
        # stuff = CommitteeTransactions.objects.all()
        # assert `stuff` has properly cleaned data
        self.fail()