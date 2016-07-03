#!/usr/bin/env python manage.py shell

"""create empty CampaignDetail records for all filer_ids in WorkingTransactions
   but not in CampaignDetail

   runs in less than a minute.
   must be run before the FK can be created linking the two tables.
   """

trans_filer_ids = set(WorkingTransactions.objects.values_list('filer_id', flat=True))
wc_filer_ids = set(WorkingCommittees.objects.values_list('committee_id', flat=True))
cd_filer_ids = set(CampaignDetail.objects.values_list('filer_id', flat=True))


for fid in trans_filer_ids:
    if fid not in cd_filer_ids:
        obj, created = CampaignDetail.objects.get_or_create(filer_id=fid)
        if created:
            obj.save()
