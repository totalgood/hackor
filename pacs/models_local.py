# 0001 - LongCharField; 2 id columns;
# 0002 - representation; primary_keys; app_label
from __future__ import unicode_literals

print('Using models in {}'.format(__file__))

from utils import models, representation


class AcGrassRootsInState(models.Model):
    filer_id = models.FloatField(blank=True, primary_key=True)
    filer = models.TextField(blank=True, null=True)
    candidate_name = models.TextField(blank=True, null=True)
    total_money = models.FloatField(blank=True, null=True)
    percent_grassroots = models.FloatField(blank=True, null=True)
    percent_instate = models.FloatField(blank=True, null=True)
    total_money_out = models.FloatField(blank=True, null=True)

    def __str__(self):
        return representation(self)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'ac_grass_roots_in_state'


class AccessLog(models.Model):
    committee_id = models.IntegerField(blank=True, primary_key=True, null=False)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return representation(self)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'access_log'


class AccessLogUpdate(models.Model):
    """Created by Daniel with rails ORM?"""
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return representation(self)

    class Meta:
        app_label = 'pacs'
        managed = False
        db_table = 'access_logs'


class AllOregonSum(models.Model):
    in_field = models.FloatField(db_column='in', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    out = models.FloatField(blank=True, null=True)
    from_within = models.FloatField(blank=True, null=True)
    to_within = models.FloatField(blank=True, null=True)
    from_outside = models.FloatField(blank=True, null=True)
    to_outside = models.FloatField(blank=True, null=True)
    total_grass_roots = models.FloatField(blank=True, null=True)
    total_from_in_state = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'all_oregon_sum'


class CampaignDetail(models.Model):
    filer_id = models.IntegerField(primary_key=True, default=0)
    candidate_name = models.TextField(blank=True, null=True)
    committee_name = models.LongCharField(max_length=-1, blank=True, null=True)
    race = models.TextField(blank=True, null=True)
    website = models.TextField(blank=True, null=True)
    phone = models.LongCharField(max_length=-1, blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    total_spent = models.FloatField(blank=True, null=True)
    grassroots = models.FloatField(blank=True, null=True)
    instate = models.FloatField(blank=True, null=True)
    filer_id = models.IntegerField(blank=True, null=True)
    election = models.TextField(blank=True, null=True)
    party = models.TextField(blank=True, null=True)
    num_transactions = models.BigIntegerField(blank=True, null=True)
    committee_type = models.LongCharField(max_length=-1, blank=True, null=True)
    committee_subtype = models.LongCharField(max_length=-1, blank=True, null=True)
    db_update_status = models.TextField(blank=True, null=True)

    IMPORTANT_FIELDS = ['filer_id', 'committee_name', 'committee_type', 'committee_subtype',
                        'candidate_name', 'website', 'party', 'race']

    def __str__(self):
        return representation(self)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'campaign_detail'


class CandidateByState(models.Model):
    candidate_name = models.TextField(blank=True, null=True)
    filer_id = models.IntegerField(blank=True, null=True)
    state = models.LongCharField(max_length=-1, blank=True, null=True)
    direction = models.CharField(max_length=7, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    def __str__(self):
        return representation(self)

    class Meta:
        verbose_name_plural = 'candidates by state'
        managed = True
        app_label = 'pacs'
        db_table = 'candidate_by_state'


class CandidateSumByDate(models.Model):
    filer_id = models.IntegerField(blank=True, primary_key=True)
    tran_date = models.DateField(blank=True, null=True)
    total_in = models.FloatField(blank=True, null=True)
    total_out = models.FloatField(blank=True, null=True)

    IMPORTANT_FIELDS = ['filer_id', 'total_in', 'total_out']

    def __str__(self):
        return representation(self)

    class Meta:
        verbose_name_plural = 'candidate sums by date'
        managed = True
        app_label = 'pacs'
        db_table = 'candidate_sum_by_date'


class CcGrassRootsInState(models.Model):
    filer_id = models.IntegerField(blank=True, primary_key=True)
    filer = models.LongCharField(max_length=-1, blank=True, null=True)
    num_transactions = models.BigIntegerField(blank=True, null=True)
    in_state = models.FloatField(blank=True, null=True)
    grass_roots = models.FloatField(blank=True, null=True)
    total_contributions = models.FloatField(blank=True, null=True)
    total_money = models.FloatField(blank=True, null=True)
    total_money_out = models.FloatField(blank=True, null=True)
    percent_grass_roots = models.FloatField(blank=True, null=True)
    percent_in_state = models.FloatField(blank=True, null=True)

    IMPORTANT_FIELDS = ['filer_id', 'filer', 'total_money', 'percent_grass_roots', 'percent_in_state']

    def __str__(self):
        return representation(self)

    class Meta:
        verbose_name = 'grass roots in-state total'
        verbose_name_plural = 'grass roots in-state totals'
        managed = True
        app_label = 'pacs'
        db_table = 'cc_grass_roots_in_state'


class CcWorkingTransactions(models.Model):
    tran_id = models.IntegerField(blank=True, primary_key=True)
    tran_date = models.DateField(blank=True, null=True)
    filer = models.LongCharField(max_length=-1, blank=True, null=True)
    contributor_payee = models.LongCharField(max_length=-1, blank=True, null=True)
    sub_type = models.LongCharField(max_length=-1, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    contributor_payee_committee_id = models.IntegerField(blank=True, null=True)
    filer_id = models.IntegerField(blank=True, null=True)
    purp_desc = models.LongCharField(max_length=-1, blank=True, null=True)
    book_type = models.LongCharField(max_length=-1, blank=True, null=True)
    addr_line1 = models.LongCharField(max_length=-1, blank=True, null=True)
    filed_date = models.DateField(blank=True, null=True)
    addr_line2 = models.LongCharField(max_length=-1, blank=True, null=True)
    city = models.LongCharField(max_length=-1, blank=True, null=True)
    state = models.LongCharField(max_length=-1, blank=True, null=True)
    zip = models.IntegerField(blank=True, null=True)
    purpose_codes = models.LongCharField(max_length=-1, blank=True, null=True)
    direction = models.CharField(max_length=7, blank=True, null=True)
    contributor_payee_class = models.LongCharField(max_length=-1, blank=True, null=True)

    IMPORTANT_FIELDS = ['tran_id', 'tran_date', 'filer_id', 'filer', 'filed_date', 'amount', 'direction', 'purpose_codes']

    def __str__(self):
        return representation(self)

    class Meta:
        verbose_name = 'working transaction'
        managed = True
        app_label = 'pacs'
        db_table = 'cc_working_transactions'


class DirectionCodes(models.Model):
    sub_type = models.LongCharField(max_length=-1, blank=True, primary_key=True)
    direction = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return representation(self)

    class Meta:
        verbose_name = 'direction'
        managed = True
        app_label = 'pacs'
        db_table = 'direction_codes'


class Documentation(models.Model):
    title = models.TextField(blank=True, null=True)
    endpoint_name = models.TextField(blank=True, null=True)
    txt = models.TextField(blank=True, null=True)

    def __str__(self):
        return representation(self)

    class Meta:
        verbose_name = 'document'
        managed = True
        app_label = 'pacs'
        db_table = 'documentation'


class HackOregonDbStatus(models.Model):
    ac_grass_roots_in_state = models.FloatField(blank=True, null=True)
    campaign_detail = models.FloatField(blank=True, null=True)
    candidate_by_state = models.FloatField(blank=True, null=True)
    candidate_sum_by_date = models.FloatField(blank=True, null=True)
    cc_grass_roots_in_state = models.FloatField(blank=True, null=True)
    cc_working_transactions = models.FloatField(blank=True, null=True)
    direction_codes = models.FloatField(blank=True, null=True)
    raw_candidate_filings = models.FloatField(blank=True, null=True)
    raw_committees = models.FloatField(blank=True, null=True)
    raw_committees_scraped = models.FloatField(blank=True, null=True)
    raw_committee_transactions = models.FloatField(blank=True, null=True)
    raw_committee_transactions_ammended_transactions = models.FloatField(blank=True, null=True)
    state_translation = models.FloatField(blank=True, null=True)
    working_candidate_committees = models.FloatField(blank=True, null=True)
    working_candidate_filings = models.FloatField(blank=True, null=True)
    working_committees = models.FloatField(blank=True, null=True)
    working_transactions = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    event_at_log_time = models.TextField(blank=True, null=True)
    hack_oregon_db_status = models.FloatField(blank=True, null=True)
    all_oregon_sum = models.FloatField(blank=True, null=True)
    state_sum_by_date = models.FloatField(blank=True, null=True)
    documentation = models.FloatField(blank=True, null=True)
    oregon_by_contributions = models.FloatField(blank=True, null=True)
    oregon_by_purpose_codes = models.FloatField(blank=True, null=True)
    sub_type_from_contributor_payee = models.FloatField(blank=True, null=True)
    oregon_committee_agg = models.FloatField(blank=True, null=True)
    import_dates = models.FloatField(blank=True, null=True)
    raw_committee_transactions_errors = models.FloatField(blank=True, null=True)
    access_log = models.FloatField(blank=True, null=True)
    search_log = models.FloatField(blank=True, null=True)

    def __str__(self):
        return representation(self)

    class Meta:
        verbose_name = 'database status'
        verbose_name_plural = 'database statuses'
        managed = True
        app_label = 'pacs'
        db_table = 'hack_oregon_db_status'


class ImportDates(models.Model):
    file_id = models.DecimalField(db_column='id', max_digits=1000, decimal_places=1000, blank=True, default=0, primary_key=True)
    scrape_date = models.DateField(blank=True, null=True)
    file_name = models.TextField(blank=True, null=True)

    def __str__(self):
        return representation(self)

    class Meta:
        verbose_name = 'file import date'
        managed = True
        app_label = 'pacs'
        db_table = 'import_dates'


class OregonByContributions(models.Model):
    contribution_type = models.LongCharField(max_length=-1, blank=True, primary_key=True)
    total = models.FloatField(blank=True, null=True)

    def __str__(self):
        return representation(self)

    class Meta:
        verbose_name = 'contribution type'
        verbose_name_plural = 'contribution types'
        managed = True
        app_label = 'pacs'
        db_table = 'oregon_by_contributions'


class OregonByPurposeCodes(models.Model):
    purpose_code = models.TextField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'oregon_by_purpose_codes'


class OregonCommitteeAgg(models.Model):
    contributor_payee = models.LongCharField(max_length=-1, blank=True, null=True)
    contributor_payee_committee_id = models.IntegerField(blank=True, null=True)
    sum = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'oregon_committee_agg'


class PacsCommitteetransactions(models.Model):
    tran_id = models.IntegerField(primary_key=True)
    original_id = models.IntegerField()
    tran_date = models.DateField(blank=True, null=True)
    tran_status = models.LongCharField(max_length=-1, blank=True, null=True)
    filer = models.LongCharField(max_length=-1, blank=True, null=True)
    contributor_payee = models.LongCharField(max_length=-1, blank=True, null=True)
    sub_type = models.LongCharField(max_length=-1, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    aggregate_amount = models.FloatField(blank=True, null=True)
    contributor_payee_committee_id = models.IntegerField(blank=True, null=True)
    filer_id = models.IntegerField(blank=True, null=True)
    attest_by_name = models.LongCharField(max_length=-1)
    attest_date = models.DateField()
    review_by_name = models.LongCharField(max_length=-1, blank=True, null=True)
    review_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    occptn_ltr_date = models.LongCharField(max_length=-1, blank=True, null=True)
    pymt_sched_txt = models.LongCharField(max_length=-1, blank=True, null=True)
    purp_desc = models.LongCharField(max_length=-1, blank=True, null=True)
    intrst_rate = models.LongCharField(max_length=-1, blank=True, null=True)
    check_nbr = models.LongCharField(max_length=-1, blank=True, null=True)
    tran_stsfd_ind = models.NullBooleanField()
    filed_by_name = models.LongCharField(max_length=-1, blank=True, null=True)
    filed_date = models.DateField(blank=True, null=True)
    addr_book_agent_name = models.LongCharField(max_length=-1, blank=True, null=True)
    book_type = models.LongCharField(max_length=-1, blank=True, null=True)
    title_txt = models.LongCharField(max_length=-1, blank=True, null=True)
    occptn_txt = models.LongCharField(max_length=-1, blank=True, null=True)
    emp_name = models.LongCharField(max_length=-1, blank=True, null=True)
    emp_city = models.LongCharField(max_length=-1, blank=True, null=True)
    emp_state = models.LongCharField(max_length=-1, blank=True, null=True)
    employ_ind = models.NullBooleanField()
    self_employ_ind = models.NullBooleanField()
    addr_line1 = models.LongCharField(max_length=-1, blank=True, null=True)
    addr_line2 = models.LongCharField(max_length=-1, blank=True, null=True)
    city = models.LongCharField(max_length=-1, blank=True, null=True)
    state = models.LongCharField(max_length=-1, blank=True, null=True)
    zip = models.IntegerField(blank=True, null=True)
    zip_plus_four = models.IntegerField(blank=True, null=True)
    county = models.LongCharField(max_length=-1, blank=True, null=True)
    purpose_codes = models.LongCharField(max_length=-1, blank=True, null=True)
    exp_date = models.LongCharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'pacs_committeetransactions'


class RawCandidateFilings(models.Model):
    election_txt = models.TextField(blank=True, null=True)
    election_year = models.IntegerField(blank=True, null=True)
    office_group = models.TextField(blank=True, null=True)
    id_nbr = models.IntegerField(blank=True, null=True)
    office = models.TextField(blank=True, null=True)
    candidate_office = models.TextField(blank=True, null=True)
    candidate_file_rsn = models.IntegerField(blank=True, null=True)
    file_mthd_ind = models.TextField(blank=True, null=True)
    filetype_descr = models.TextField(blank=True, null=True)
    party_descr = models.TextField(blank=True, null=True)
    major_party_ind = models.TextField(blank=True, null=True)
    cand_ballot_name_txt = models.TextField(blank=True, null=True)
    occptn_txt = models.TextField(blank=True, null=True)
    education_bckgrnd_txt = models.TextField(blank=True, null=True)
    occptn_bkgrnd_txt = models.TextField(blank=True, null=True)
    school_grade_diploma_degree_certificate_course_of_study = models.TextField(blank=True, null=True)
    prev_govt_bkgrnd_txt = models.TextField(blank=True, null=True)
    judge_incbnt_ind = models.TextField(blank=True, null=True)
    qlf_ind = models.TextField(blank=True, null=True)
    filed_date = models.DateField(blank=True, null=True)
    file_fee_rfnd_date = models.DateField(blank=True, null=True)
    witdrw_date = models.DateField(blank=True, null=True)
    withdrw_resn_txt = models.NullBooleanField()
    pttn_file_date = models.DateField(blank=True, null=True)
    pttn_sgnr_rqd_nbr = models.IntegerField(blank=True, null=True)
    pttn_signr_filed_nbr = models.IntegerField(blank=True, null=True)
    pttn_cmplt_date = models.DateField(blank=True, null=True)
    ballot_order_nbr = models.IntegerField(blank=True, null=True)
    prfx_name_cd = models.TextField(blank=True, null=True)
    first_name = models.TextField(blank=True, null=True)
    mdle_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    sufx_name = models.TextField(blank=True, null=True)
    title_txt = models.TextField(blank=True, null=True)
    mailing_addr_line_1 = models.TextField(blank=True, null=True)
    mailing_addr_line_2 = models.TextField(blank=True, null=True)
    mailing_city_name = models.TextField(blank=True, null=True)
    mailing_st_cd = models.TextField(blank=True, null=True)
    mailing_zip_code = models.IntegerField(blank=True, null=True)
    mailing_zip_plus_four = models.IntegerField(blank=True, null=True)
    residence_addr_line_1 = models.TextField(blank=True, null=True)
    residence_addr_line_2 = models.TextField(blank=True, null=True)
    residence_city_name = models.TextField(blank=True, null=True)
    residence_st_cd = models.TextField(blank=True, null=True)
    residence_zip_code = models.IntegerField(blank=True, null=True)
    residence_zip_plus_four = models.IntegerField(blank=True, null=True)
    home_phone = models.TextField(blank=True, null=True)
    cell_phone = models.TextField(blank=True, null=True)
    fax_phone = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    work_phone = models.TextField(blank=True, null=True)
    web_address = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'raw_candidate_filings'


class RawCommitteeTransactions(models.Model):
    tran_id = models.IntegerField(blank=True, null=True)
    original_id = models.IntegerField(blank=True, null=True)
    tran_date = models.DateField(blank=True, null=True)
    tran_status = models.LongCharField(max_length=-1, blank=True, null=True)
    filer = models.LongCharField(max_length=-1, blank=True, null=True)
    contributor_payee = models.LongCharField(max_length=-1, blank=True, null=True)
    sub_type = models.LongCharField(max_length=-1, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    aggregate_amount = models.FloatField(blank=True, null=True)
    contributor_payee_committee_id = models.IntegerField(blank=True, null=True)
    filer_id = models.IntegerField(blank=True, null=True)
    attest_by_name = models.LongCharField(max_length=-1, blank=True, null=True)
    attest_date = models.DateField(blank=True, null=True)
    review_by_name = models.LongCharField(max_length=-1, blank=True, null=True)
    review_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    occptn_ltr_date = models.LongCharField(max_length=-1, blank=True, null=True)
    pymt_sched_txt = models.LongCharField(max_length=-1, blank=True, null=True)
    purp_desc = models.LongCharField(max_length=-1, blank=True, null=True)
    intrst_rate = models.LongCharField(max_length=-1, blank=True, null=True)
    check_nbr = models.LongCharField(max_length=-1, blank=True, null=True)
    tran_stsfd_ind = models.NullBooleanField()
    filed_by_name = models.LongCharField(max_length=-1, blank=True, null=True)
    filed_date = models.DateField(blank=True, null=True)
    addr_book_agent_name = models.LongCharField(max_length=-1, blank=True, null=True)
    book_type = models.LongCharField(max_length=-1, blank=True, null=True)
    title_txt = models.LongCharField(max_length=-1, blank=True, null=True)
    occptn_txt = models.LongCharField(max_length=-1, blank=True, null=True)
    emp_name = models.LongCharField(max_length=-1, blank=True, null=True)
    emp_city = models.LongCharField(max_length=-1, blank=True, null=True)
    emp_state = models.LongCharField(max_length=-1, blank=True, null=True)
    employ_ind = models.NullBooleanField()
    self_employ_ind = models.NullBooleanField()
    addr_line1 = models.LongCharField(max_length=-1, blank=True, null=True)
    addr_line2 = models.LongCharField(max_length=-1, blank=True, null=True)
    city = models.LongCharField(max_length=-1, blank=True, null=True)
    state = models.LongCharField(max_length=-1, blank=True, null=True)
    zip = models.IntegerField(blank=True, null=True)
    zip_plus_four = models.IntegerField(blank=True, null=True)
    county = models.LongCharField(max_length=-1, blank=True, null=True)
    purpose_codes = models.LongCharField(max_length=-1, blank=True, null=True)
    exp_date = models.LongCharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'raw_committee_transactions'


class RawCommitteeTransactionsAmmendedTransactions(models.Model):
    tran_id = models.IntegerField(blank=True, null=True)
    original_id = models.IntegerField(blank=True, null=True)
    tran_date = models.DateField(blank=True, null=True)
    tran_status = models.LongCharField(max_length=-1, blank=True, null=True)
    filer = models.LongCharField(max_length=-1, blank=True, null=True)
    contributor_payee = models.LongCharField(max_length=-1, blank=True, null=True)
    sub_type = models.LongCharField(max_length=-1, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    aggregate_amount = models.FloatField(blank=True, null=True)
    contributor_payee_committee_id = models.IntegerField(blank=True, null=True)
    filer_id = models.IntegerField(blank=True, null=True)
    attest_by_name = models.LongCharField(max_length=-1, blank=True, null=True)
    attest_date = models.DateField(blank=True, null=True)
    review_by_name = models.LongCharField(max_length=-1, blank=True, null=True)
    review_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    occptn_ltr_date = models.LongCharField(max_length=-1, blank=True, null=True)
    pymt_sched_txt = models.LongCharField(max_length=-1, blank=True, null=True)
    purp_desc = models.LongCharField(max_length=-1, blank=True, null=True)
    intrst_rate = models.LongCharField(max_length=-1, blank=True, null=True)
    check_nbr = models.LongCharField(max_length=-1, blank=True, null=True)
    tran_stsfd_ind = models.NullBooleanField()
    filed_by_name = models.LongCharField(max_length=-1, blank=True, null=True)
    filed_date = models.DateField(blank=True, null=True)
    addr_book_agent_name = models.LongCharField(max_length=-1, blank=True, null=True)
    book_type = models.LongCharField(max_length=-1, blank=True, null=True)
    title_txt = models.LongCharField(max_length=-1, blank=True, null=True)
    occptn_txt = models.LongCharField(max_length=-1, blank=True, null=True)
    emp_name = models.LongCharField(max_length=-1, blank=True, null=True)
    emp_city = models.LongCharField(max_length=-1, blank=True, null=True)
    emp_state = models.LongCharField(max_length=-1, blank=True, null=True)
    employ_ind = models.NullBooleanField()
    self_employ_ind = models.NullBooleanField()
    addr_line1 = models.LongCharField(max_length=-1, blank=True, null=True)
    addr_line2 = models.LongCharField(max_length=-1, blank=True, null=True)
    city = models.LongCharField(max_length=-1, blank=True, null=True)
    state = models.LongCharField(max_length=-1, blank=True, null=True)
    zip = models.IntegerField(blank=True, null=True)
    zip_plus_four = models.IntegerField(blank=True, null=True)
    county = models.LongCharField(max_length=-1, blank=True, null=True)
    purpose_codes = models.LongCharField(max_length=-1, blank=True, null=True)
    exp_date = models.LongCharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'raw_committee_transactions_ammended_transactions'


class RawCommitteeTransactionsErrors(models.Model):
    tran_id = models.IntegerField(blank=True, null=True)
    original_id = models.IntegerField(blank=True, null=True)
    tran_date = models.DateField(blank=True, null=True)
    tran_status = models.LongCharField(max_length=-1, blank=True, null=True)
    filer = models.LongCharField(max_length=-1, blank=True, null=True)
    contributor_payee = models.LongCharField(max_length=-1, blank=True, null=True)
    sub_type = models.LongCharField(max_length=-1, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    aggregate_amount = models.FloatField(blank=True, null=True)
    contributor_payee_committee_id = models.IntegerField(blank=True, null=True)
    filer_id = models.IntegerField(blank=True, null=True)
    attest_by_name = models.LongCharField(max_length=-1, blank=True, null=True)
    attest_date = models.DateField(blank=True, null=True)
    review_by_name = models.LongCharField(max_length=-1, blank=True, null=True)
    review_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    occptn_ltr_date = models.LongCharField(max_length=-1, blank=True, null=True)
    pymt_sched_txt = models.LongCharField(max_length=-1, blank=True, null=True)
    purp_desc = models.LongCharField(max_length=-1, blank=True, null=True)
    intrst_rate = models.LongCharField(max_length=-1, blank=True, null=True)
    check_nbr = models.LongCharField(max_length=-1, blank=True, null=True)
    tran_stsfd_ind = models.NullBooleanField()
    filed_by_name = models.LongCharField(max_length=-1, blank=True, null=True)
    filed_date = models.DateField(blank=True, null=True)
    addr_book_agent_name = models.LongCharField(max_length=-1, blank=True, null=True)
    book_type = models.LongCharField(max_length=-1, blank=True, null=True)
    title_txt = models.LongCharField(max_length=-1, blank=True, null=True)
    occptn_txt = models.LongCharField(max_length=-1, blank=True, null=True)
    emp_name = models.LongCharField(max_length=-1, blank=True, null=True)
    emp_city = models.LongCharField(max_length=-1, blank=True, null=True)
    emp_state = models.LongCharField(max_length=-1, blank=True, null=True)
    employ_ind = models.NullBooleanField()
    self_employ_ind = models.NullBooleanField()
    addr_line1 = models.LongCharField(max_length=-1, blank=True, null=True)
    addr_line2 = models.LongCharField(max_length=-1, blank=True, null=True)
    city = models.LongCharField(max_length=-1, blank=True, null=True)
    state = models.LongCharField(max_length=-1, blank=True, null=True)
    zip = models.IntegerField(blank=True, null=True)
    zip_plus_four = models.IntegerField(blank=True, null=True)
    county = models.LongCharField(max_length=-1, blank=True, null=True)
    purpose_codes = models.LongCharField(max_length=-1, blank=True, null=True)
    exp_date = models.LongCharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'raw_committee_transactions_errors'


class RawCommittees(models.Model):
    committee_id = models.IntegerField(blank=True, null=True)
    committee_name = models.LongCharField(max_length=-1, blank=True, null=True)
    committee_type = models.LongCharField(max_length=-1, blank=True, null=True)
    committee_subtype = models.LongCharField(max_length=-1, blank=True, null=True)
    candidate_office = models.LongCharField(max_length=-1, blank=True, null=True)
    candidate_office_group = models.LongCharField(max_length=-1, blank=True, null=True)
    filing_date = models.DateField(blank=True, null=True)
    organization_filing_date = models.DateField(db_column='organization_filing Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    treasurer_first_name = models.LongCharField(max_length=-1, blank=True, null=True)
    treasurer_last_name = models.LongCharField(max_length=-1, blank=True, null=True)
    treasurer_mailing_address = models.LongCharField(max_length=-1, blank=True, null=True)
    treasurer_work_phone = models.LongCharField(max_length=-1, blank=True, null=True)
    treasurer_fax = models.LongCharField(max_length=-1, blank=True, null=True)
    candidate_first_name = models.LongCharField(max_length=-1, blank=True, null=True)
    candidate_last_name = models.LongCharField(max_length=-1, blank=True, null=True)
    candidate_maling_address = models.LongCharField(max_length=-1, blank=True, null=True)
    candidate_work_phone = models.LongCharField(max_length=-1, blank=True, null=True)
    candidate_residence_phone = models.LongCharField(max_length=-1, blank=True, null=True)
    candidate_fax = models.LongCharField(max_length=-1, blank=True, null=True)
    candidate_email = models.LongCharField(max_length=-1, blank=True, null=True)
    active_election = models.LongCharField(max_length=-1, blank=True, null=True)
    measure = models.LongCharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'raw_committees'


class RawCommitteesScraped(models.Model):
    name = models.TextField(blank=True, null=True)
    committee_id = models.IntegerField(db_column='id', blank=True, null=False, default=0, primary_key=True)
    acronym = models.TextField(blank=True, null=True)
    pac_type = models.TextField(blank=True, null=True)
    filing_effective_from = models.TextField(blank=True, null=True)
    filing_type = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    campaign_phone = models.TextField(blank=True, null=True)
    treasurer_name = models.TextField(blank=True, null=True)
    treasurer_mailing_address = models.TextField(blank=True, null=True)
    treasurer_work_phone_home_phone_fax = models.TextField(blank=True, null=True)
    treasurer_email_address = models.TextField(blank=True, null=True)
    candidate_name = models.TextField(blank=True, null=True)
    candidate_election_office = models.TextField(blank=True, null=True)
    candidate_party_affiliation = models.TextField(blank=True, null=True)
    candidate_candidate_address = models.TextField(blank=True, null=True)
    candidate_work_phone_home_phone_fax = models.TextField(blank=True, null=True)
    candidate_mailing_address = models.TextField(blank=True, null=True)
    candidate_email_address = models.TextField(blank=True, null=True)
    candidate_occupation = models.TextField(blank=True, null=True)
    candidate_employer = models.TextField(blank=True, null=True)
    measure_election = models.TextField(blank=True, null=True)
    measure_support = models.TextField(blank=True, null=True)
    measure_details = models.TextField(blank=True, null=True)
    committee_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'raw_committees_scraped'


class SearchLog(models.Model):
    search_term = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'search_log'


class StateSumByDate(models.Model):
    tran_date = models.DateField(blank=True, null=True)
    total_in = models.FloatField(blank=True, null=True)
    total_out = models.FloatField(blank=True, null=True)
    total_from_within = models.FloatField(blank=True, null=True)
    total_to_within = models.FloatField(blank=True, null=True)
    total_from_the_outside = models.FloatField(blank=True, null=True)
    total_to_the_outside = models.FloatField(blank=True, null=True)
    total_grass_roots = models.FloatField(blank=True, null=True)
    total_from_in_state = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'state_sum_by_date'


class StateTranslation(models.Model):
    statefull = models.LongCharField(max_length=-1, blank=True, null=True)
    abbreviation = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'state_translation'


class SubTypeFromContributorPayee(models.Model):
    contributor_payee = models.LongCharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'sub_type_from_contributor_payee'


class WorkingCandidateCommittees(models.Model):
    candidate_name = models.TextField(blank=True, null=True)
    committee_id = models.IntegerField(blank=True, null=True)
    committee_name = models.LongCharField(max_length=-1, blank=True, null=True)
    election_office = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    party_affiliation = models.TextField(blank=True, null=True)
    web_address = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'working_candidate_committees'


class WorkingCandidateFilings(models.Model):
    election_txt = models.TextField(blank=True, null=True)
    election_year = models.IntegerField(blank=True, null=True)
    office_group = models.TextField(blank=True, null=True)
    id_nbr = models.IntegerField(blank=True, null=True)
    office = models.TextField(blank=True, null=True)
    candidate_office = models.TextField(blank=True, null=True)
    candidate_file_rsn = models.IntegerField(blank=True, null=True)
    file_mthd_ind = models.TextField(blank=True, null=True)
    filetype_descr = models.TextField(blank=True, null=True)
    party_descr = models.TextField(blank=True, null=True)
    major_party_ind = models.TextField(blank=True, null=True)
    cand_ballot_name_txt = models.TextField(blank=True, null=True)
    occptn_txt = models.TextField(blank=True, null=True)
    education_bckgrnd_txt = models.TextField(blank=True, null=True)
    occptn_bkgrnd_txt = models.TextField(blank=True, null=True)
    school_grade_diploma_degree_certificate_course_of_study = models.TextField(blank=True, null=True)
    prev_govt_bkgrnd_txt = models.TextField(blank=True, null=True)
    judge_incbnt_ind = models.TextField(blank=True, null=True)
    qlf_ind = models.TextField(blank=True, null=True)
    filed_date = models.DateField(blank=True, null=True)
    file_fee_rfnd_date = models.DateField(blank=True, null=True)
    witdrw_date = models.DateField(blank=True, null=True)
    withdrw_resn_txt = models.NullBooleanField()
    pttn_file_date = models.DateField(blank=True, null=True)
    pttn_sgnr_rqd_nbr = models.IntegerField(blank=True, null=True)
    pttn_signr_filed_nbr = models.IntegerField(blank=True, null=True)
    pttn_cmplt_date = models.DateField(blank=True, null=True)
    ballot_order_nbr = models.IntegerField(blank=True, null=True)
    prfx_name_cd = models.TextField(blank=True, null=True)
    first_name = models.TextField(blank=True, null=True)
    mdle_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    sufx_name = models.TextField(blank=True, null=True)
    title_txt = models.TextField(blank=True, null=True)
    mailing_addr_line_1 = models.TextField(blank=True, null=True)
    mailing_addr_line_2 = models.TextField(blank=True, null=True)
    mailing_city_name = models.TextField(blank=True, null=True)
    mailing_st_cd = models.TextField(blank=True, null=True)
    mailing_zip_code = models.IntegerField(blank=True, null=True)
    mailing_zip_plus_four = models.IntegerField(blank=True, null=True)
    residence_addr_line_1 = models.TextField(blank=True, null=True)
    residence_addr_line_2 = models.TextField(blank=True, null=True)
    residence_city_name = models.TextField(blank=True, null=True)
    residence_st_cd = models.TextField(blank=True, null=True)
    residence_zip_code = models.IntegerField(blank=True, null=True)
    residence_zip_plus_four = models.IntegerField(blank=True, null=True)
    home_phone = models.TextField(blank=True, null=True)
    cell_phone = models.TextField(blank=True, null=True)
    fax_phone = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    work_phone = models.TextField(blank=True, null=True)
    web_address = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'working_candidate_filings'


class WorkingCommittees(models.Model):
    committee_id = models.IntegerField(blank=True, null=True)
    committee_name = models.LongCharField(max_length=-1, blank=True, null=True)
    committee_type = models.LongCharField(max_length=-1, blank=True, null=True)
    committee_subtype = models.LongCharField(max_length=-1, blank=True, null=True)
    party_affiliation = models.TextField(blank=True, null=True)
    phone = models.LongCharField(max_length=-1, blank=True, null=True)
    election_office = models.TextField(blank=True, null=True)
    candidate_name = models.TextField(blank=True, null=True)
    candidate_email_address = models.LongCharField(max_length=-1, blank=True, null=True)
    candidate_work_phone_home_phone_fax = models.TextField(blank=True, null=True)
    candidate_address = models.LongCharField(max_length=-1, blank=True, null=True)
    treasurer_name = models.TextField(blank=True, null=True)
    treasurer_work_phone_home_phone_fax = models.TextField(blank=True, null=True)
    treasurer_mailing_address = models.LongCharField(max_length=-1, blank=True, null=True)
    web_address = models.TextField(blank=True, null=True)
    measure = models.LongCharField(max_length=-1, blank=True, null=True)
    simple_election = models.TextField(blank=True, null=True)
    db_update_status = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'working_committees'


class WorkingTransactions(models.Model):
    tran_id = models.IntegerField(blank=True, null=True)
    tran_date = models.DateField(blank=True, null=True)
    filer = models.LongCharField(max_length=-1, blank=True, null=True)
    contributor_payee = models.LongCharField(max_length=-1, blank=True, null=True)
    sub_type = models.LongCharField(max_length=-1, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    contributor_payee_committee_id = models.IntegerField(blank=True, null=True)
    filer_id = models.IntegerField(blank=True, null=True)
    purp_desc = models.LongCharField(max_length=-1, blank=True, null=True)
    book_type = models.LongCharField(max_length=-1, blank=True, null=True)
    addr_line1 = models.LongCharField(max_length=-1, blank=True, null=True)
    filed_date = models.DateField(blank=True, null=True)
    addr_line2 = models.LongCharField(max_length=-1, blank=True, null=True)
    city = models.LongCharField(max_length=-1, blank=True, null=True)
    state = models.LongCharField(max_length=-1, blank=True, null=True)
    zip = models.IntegerField(blank=True, null=True)
    purpose_codes = models.LongCharField(max_length=-1, blank=True, null=True)
    direction = models.CharField(max_length=7, blank=True, null=True)
    contributor_payee_class = models.LongCharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pacs'
        db_table = 'working_transactions'
