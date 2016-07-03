import os

import pandas as pd

from django.db.models import Sum
from django.apps import apps
from django_pandas.io import read_frame

from utils import models
from pacs.models import RawCommitteeTransactions


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


def get_model(table=None, app=None):
    """Retrieve a Django model based on the model class name

    TODO: fuzzy match on all the model._meta.db_table names and model.__class__ names
    """
    if isinstance(table, models.Model):
        return table
    if table is None:
        table = ''
    if isinstance(table, basestring):
        if '.' in table:
            table = table.split('.')
            app = '.'.join(table[:-1])
            table = table[-1]
        if app is None:
            app = os.path.split(os.path.basedir(__file__))[-1]
        if isinstance(app, basestring):
            app = apps.get_app_config(app)
        return app.models.get(table, app.models.iteritems().next()[1])
    return table


def df_from_model(table=RawCommitteeTransactions, app='pacs'):
    if isinstance(table, pd.DataFrame):
        return table
    if not hasattr(table, 'all'):
        if not hasattr(table, 'objects'):
            table = get_model(table=table, app=app)
        table = table.objects
    table = table.all()
    return read_frame(table)


def corpus_from_table(df='RawCommittee', verbosity=None):
    df = df_from_model()
    names = df.index.values
    corpus = [' '.join(str(f) for f in fields) for fields in
              zip(*[df[col] for col in df.columns if df[col].dtype == pd.np.dtype('O')])]
    if verbosity:
        print(corpus[:3])
    return pd.DataFrame(corpus, index=names, columns=['text'])


def cov_from_corpus(corpus=None, verbosity=None):
    names = corpus.index.values
    vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), stop_words='english')
    # rows should be documents, columns should be "words"
    vectors = vectorizer.fit(corpus)
    tfidf = vectors.transform(corpus)
    # tfidf_df = pd.DataFrame(tfidf.todense(), index=names)
    # print(dir(tfidf))

    cov_df = cov_from_tfidf(tfidf, names=names)
    if verbosity:
        print(cov_df.describe())
    return cov_df


def cov_from_tfidf(tfidf, names=None, verbosity=None):
    cov = tfidf * tfidf.T
    if names is None:
        names = np.arange(0, cov.shape[0])
    if verbosity:
        print(names)
        print(cov)
    return pd.DataFrame(cov.todense(), columns=names, index=names)


# pacs_scraped = pd.DataFrame.from_csv('data/public.raw_committees_scraped.csv')  # id
# pacs = pd.DataFrame.from_csv('data/public.raw_committees.csv')  # no ID that I can find
# candidates = pd.DataFrame.from_csv('data/public.raw_candidate_filings.csv')  # id_nmbr
# print(pacs_scraped.info())
# print(candidates.info())

# df = pacs_scraped
# names = df.index.values
# corpus = [' '.join(str(f) for f in fields) for fields in
#           zip(*[df[col] for col in df.columns if df[col].dtype == pd.np.dtype('O')])]
# print(corpus[:3])
# vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 1), stop_words='english')
# # rows should be documents, columns should be "words"
# vectors = vectorizer.fit(corpus)
# tfidf = vectors.transform(corpus)
# tfidf_df = pd.DataFrame(tfidf.todense(), index=names)
# # print(dir(tfidf))
# cov = tfidf * tfidf.T
# cov_df = pd.DataFrame(cov.todense(), columns=names, index=names)

# print(cov_df.describe())

# party in raw_candidate_filings


corpus = corpus_from_table(verbosity=1)
cov = cov_from_corpus(corpus)


def json_from_cov_df(df=cov, threshold=.5):
    """Produce a json string describing the graph (list of edges) from a square auto-correlation/covariance matrix

       { "nodes": [{"group": 1, "name": "the"},
                {"group": 1, "name": "and"},
                {"group": 1, "name": "our"},
                {"group": 2, "name": "that"},...
         "links": [{"source": 0, "target": 0, "value": 2.637520131294177},
                   {"source": 0, "target": 1, "value": 1.343999676850537}, ...
    """
    nodes = [{'group': 1, "name": name} for name in df.index.values()]
    edges = []
    for i, (row_name, row) in enumerate(df.iterrows()):
        for j, value in enumerate(row.values):
            if i > j:
                edges += [{'source': i, 'target': j, 'value': value}]
    return json.dumps([{'nodes': nodes, 'links': edges}])


if __name__ == '__main__':
    pass
    # print(corpus)