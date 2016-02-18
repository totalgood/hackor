import re
import os
from collections import Counter
from itertools import chain

import pandas as pd
np = pd.np
np.norm = np.linalg.norm
from datetime import datetime, date
import json

# see data/*.ipynb for more recent, working code

# import matplotlib
# import sklearn
# from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer  # equivalent to TFIDFTransformer(CountVectorizer())

# # typical linear classifier
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

# df_amounts = pd.DataFrame(df['net_amount'], index=


def cov_from_column(df=CampaignDetail, n=500, index='committee_name', values='net_amount'):
    """totally worthless function, just us Pandas column.std()**2"""
    if index is None:
        index = df.index.values
    if values is None:
        values = df[df.columns[-1]].values
    if isinstance(index, (basestring, int, float)):
        index = df[index].values
    if isinstance(values, (basestring, int, float)):
        values = df[values].values
    # dropna if either index or value is NaN
    df2 = pd.DataFrame()
    df2['label'] = index
    df2['value'] = values
    df2 = df2[index.astype('bool')][['label', 'value']].dropna(how='all')
    values = df2['value']
    cov = values * values.T
    return pd.DataFrame(cov.todense(), columns=index, index=index)


def df_from_table(table=None, verbosity=0):
    if table is None:
        table = '../data/public.working_committees.csv'
    if hasattr(table, 'objects'):
        table = table.objects
    if hasattr(table, 'filter') and callable(table.values):
        table = pd.DataFrame.from_records(table.values().all())
    if isinstance(table, basestring) and os.path.isfile(table):
        table = pd.DataFrame.from_csv(table)
    return table


def corpus_from_table(table=None,
                      bad_words=set(['nan', 'null', 'none']),
                      # FIXME: prevent words from ending with nonalphanum (hyphen, underscore)
                      word_regex=re.compile(r'^[a-zA-Z][-_a-zA-Z]*$'),
                      split_regex=re.compile(r'[^-a-zA-Z0-9]+[-_0-9]*'),
                      verbosity=0,
                      ):
    """Return a list of strings/documents from concatenated + stringified table rows"""
    word_regex, split_regex = [re.compile(regex) if isinstance(regex, basestring) else regex
                               for regex in (word_regex, split_regex)]
    df = df_from_table(table, verbosity=verbosity)
    corpus = [' '.join(str(f) for f in fields if
              (not isinstance(f, (float, int, datetime, date, np.int_, np.float_))
               and f is not None and f is not np.nan))
              for fields in zip(*[df[col] for col in df.columns
              if df[col].dtype == pd.np.dtype('O')])]
    # 2nd pass to exclude dates, numbers, "nan"s (let nltk and sklearn handle stop words)
    corpus = [' '.join(token for token in split_regex.split(doc)
              if word_regex.match(token) and token.lower() not in bad_words)
              for doc in corpus]
    return corpus


def cov_from_table(table=None, verbosity=0):
    # pacs = pd.DataFrame.from_csv('../data/public.raw_committees.csv')  # no ID that I can find
    # print(pacs_scraped.info())
    # print(candidates.info())
    corpus = corpus_from_table(table, verbosity=verbosity)
    tf = Counter(chain(*[doc.split() for doc in corpus]))
    if verbosity > 0:
        print tf.most_common()[:20]

    vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), stop_words='english')

    # rows are "documents", columns are "words"
    vectors = vectorizer.fit(corpus)
    tfidf = vectors.transform(corpus)
    # tfidf_df = pd.DataFrame(tfidf.todense(), index=names)
    cov = tfidf * tfidf.T
    # FIXME: is todense() required?
    return pd.DataFrame(cov.todense(), columns=df.index, index=df.index)


CLASSES = ["", "Whig", "Dem", "Rep", "Dem-Rep", "Fed", "Indie"]
CLASSES = dict(zip(CLASSES, range(len(CLASSES))))


# FIXME: need to create a dict or Pandas Index of node names and their d3 group index (0-N)
def graph_from_cov_df(df, threshold=.5, gain=2., n=None, class_dict=CLASSES):
    """Compose pair of lists of dicts (nodes, edges) for the graph described by a DataFrame"""
    n = n or len(df)
    nodes = [{'group': class_dict.get(name, 0), "name": name} for name in df.index.values][:n]
    edges = []
    for i, (row_name, row) in enumerate(df.iterrows()):
        for j, value in enumerate(row.values):
            if i > j and value * gain > threshold and i < n and j < n:
                edges += [{'source': i, 'target': j, 'value': gain * value}]
    return nodes, edges


def json_from_cov_df(df, threshold=.5, gain=2., n=None, indent=1):
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
    js = json_from_cov_df(df=)
    if verbosity:
        print(js[:1000] + '\n...\n' + js[-1000:])
    with open(filename, 'w') as f:
        f.write(js)


if __name__ == '__main__':
    main()
