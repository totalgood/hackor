filer_ids = set(RawCommitteeTransactions.objects.values_list('filer_id', flat=True).distinct())
payee_ids = set(RawCommitteeTransactions.objects.values_list('contributor_payee_committee_id', flat=True).distinct())
committee_ids = set(RawCommittees.objects.values_list('committee_id', flat=True).distinct())

len(committee_ids.intersection(payee_ids))
# 1025
len(committee_ids.intersection(filer_ids))
# 1812
len(committee_ids.intersection(filer_ids)) /float(len(filer_ids))
# 0.5541284403669725
len(committee_ids.intersection(payee_ids)) / float(len(payee_ids))
# 0.5349686847599165
len(committee_ids.intersection(payee_ids)) / float(len(committee_ids))
# 0.3948382126348228
len(committee_ids.intersection(filer_ids)) / float(len(committee_ids))
# 0.6979969183359014
