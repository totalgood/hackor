import re
import pandas as pd
np = pd.np
np.norm = np.linalg.norm
from datetime import datetime, date
import json

# import matplotlib
# import sklearn
# from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer  # equivalent to TFIDFTransformer(CountVectorizer())

# typical linear classifier
# from sklearn.linear_model import SGDClassifier
# from sklearn.grid_search import GridSearchCV
# from sklearn.pipeline import Pipeline
# from sklearn.cross_validation import train_test_split

from django.db.models import Sum

from pacs.models import CampaignDetail

# the net_amount column doesn't appear in the df unless you use the plain old df.from_records method
# from django_pandas.io import read_frame
# qs = CampaignDetail.objects.annotate(net_amount=Sum('workingtransactions__amount'))
# df_no_net = read_frame(qs)

# Django queries
# this is how you do a join between the CampaignDetail table and WorkingTransactions table
#   and aggregate only the "amount" on the Transactions table
qs = CampaignDetail.objects.annotate(net_amount=Sum('workingtransactions__amount')).values().all()

# this is one easy way to convert a django queryset into a Pandas dataframe
df = pd.DataFrame.from_records(qs)

# What if you only want the positive transactions summed
qs_pos = CampaignDetail.objects.filter(workingtransactions__amount__gt=0)
qs_pos = qs_pos.annotate(pos_amount=Sum('workingtransactions__amount'))

# this is how you do a join on a pandas dataframe
df_pos = df.join(pd.DataFrame.from_records(qs_pos.values('pos_amount').all())['pos_amount'])

# but what if I just inserted a new column into the dataframe with the values I want
df['pos_amount'] = pd.DataFrame.from_records(qs_pos.values('pos_amount').all())['pos_amount']

# Did all the rows get inserted in the right place (are the indices still alligned)
print((df == df_pos))
print((df == df_pos).mean())
# it turns out that a NaN is not equal to a NaN
# any operation involving a NaN returns a NaN
# and NaN (like None) always evaluates to False
print((df == df_pos).mean() + df.isnull().mean())

# get rid of rows without a committee name (from transactions with filer_id not in CampaignDetail)
df = df[df.committee_name.astype(bool)].copy()
df = df.set_index(df.committee_name)

# lets do it all again for negative transaction amounts
qs_neg = CampaignDetail.objects.filter(workingtransactions__amount__lt=0)
qs_neg = qs_neg.annotate(neg_amount=Sum('workingtransactions__amount'))
df = df.join(pd.DataFrame.from_records(qs_pos.values('neg_amount').all())['neg_amount'])


# Can we create a directed graph of financial transactions between committees?
# are the payee_committee_ids the same as "filer_id"?
filer_id = set(pd.DataFrame.from_records(WorkingTransactions.objects.values(
               'filer_id').all()).dropna().values.T[0])
payee_id = set(pd.DataFrame.from_records(WorkingTransactions.objects.values(
               'contributor_payee_committee_id').all()).dropna().values.T[0])
print(len(payee_id.intersection(filer_id)) * 1. / len(filer_id))

# That's good enough for government work


def transaction_matrix():
    pass


def df_cov_from_df(df, n=500, index_label='committee_name', value_labels=['net_amount']):
    value_labels = list(value_labels)
    df = df[df[index_label].astype('bool')][[index_label] + list(value_labels)].dropna(how='all')
    names = df[index_label].values
    values = df[value_labels].values
    cov = np.matrix(values) * np.matrix(values).T
    diag = np.diag(np.diagonal(cov) ** -.5)
    return pd.DataFrame(diag * cov * diag, columns=names, index=names)


#df = pd.DataFrame.from_csv('../data/public.working_committees.csv')  # id
# pacs = pd.DataFrame.from_csv('../data/public.raw_committees.csv')  # no ID that I can find
# print(pacs_scraped.info())
# print(candidates.info())

names = df.index.values
corpus = [' '.join(str(f) for f in fields if
                   (not isinstance(f, (float, int, datetime, date, np.int_, np.float_)) and not f in (None, np.nan)))
          for fields in zip(*[df[col] for col in df.columns if df[col].dtype == pd.np.dtype('O')])]
print(corpus[:3])

from collections import Counter
from itertools import chain
tf = Counter(chain(*[doc.split() for doc in corpus]))
print(tf.most_common(10))

# so we need to exclude dates and numbers and "nan"s (we'll let nltk and sklearn handle stop words)
bad_words = set(['nan'])
regex = re.compile(r'^[a-zA-Z][-_a-zA-Z]*[a-zA-Z0-9][!.?]*$')
corpus = [' '.join(token for token in doc.split() if regex.match(token) and token not in bad_words)
          for doc in corpus]

vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), stop_words='english')

# rows are "documents", columns are "words"
vectors = vectorizer.fit(corpus)
tfidf = vectors.transform(corpus)
tfidf_df = pd.DataFrame(tfidf.todense(), index=names)
cov = tfidf * tfidf.T
cov_df = pd.DataFrame(cov.todense(), columns=names, index=names)


parties = ["", "Whig", "Dem", "Rep", "Dem-Rep", "Fed", "Indie"]
groups = {"": 0, "Whig": 1, "Dem": 2, "Rep": 3, "Dem-Rep": 4, "Fed": 5, "Indie": 6}


def graph_from_cov_df(df=cov_df, threshold=.5, gain=2., n=300):
    """Compose pair of lists of dicts (nodes, edges) for the graph described by a DataFrame"""

    nodes = [{'group': 0, "name": name} for name in df.index.values][:n]
    edges = []
    for i, (row_name, row) in enumerate(df.iterrows()):
        for j, value in enumerate(row.values):
            if i > j and value * gain > threshold and i < n and j < n:
                edges += [{'source': i, 'target': j, 'value': gain * value}]
    return nodes, edges


def json_from_cov_df(df=cov_df, threshold=.5, gain=2., n=300, indent=1):
    """Produce a json string describing the graph (list of edges) from a square auto-correlation/covariance matrix

       { "nodes": [{"group": 1, "name": "the"},
                {"group": 1, "name": "and"},
                {"group": 1, "name": "our"},
                {"group": 2, "name": "that"},...
         "links": [{"source": 0, "target": 0, "value": 2.637520131294177},
                   {"source": 0, "target": 1, "value": 1.343999676850537}, ...
    """
    nodes, edges = graph_from_cov_df(df=df, threshold=threshold, gain=gain, n=n)
    return json.dumps({'nodes': nodes, 'links': edges}, indent=indent)


def main(filename='nlp_similarity_graph.json', verbosity=1):
    js = json_from_cov_df()
    if verbosity:
        print(js[:1000] + '\n...\n' + js[-1000:])
    with open(filename, 'w') as f:
        f.write(js)


if __name__ == '__main__':
    main()
