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

qs = CampaignDetail.objects.annotate(net_amount=Sum('workingtransactions__amount')).values().all()
df = pd.DataFrame.from_records()
df_amounts = pd.DataFrame(df['net_amount'], index=

def df_cov_from_df(df, n=500, index_label='committee_name', value_label='net_amount'):
    df = df[df[index_label].astype('bool')][[index_label, value_label]].dropna(how='all')
    names = df[index_label].values
    values = df[value_label].values
    cov = np.matrix(values).T * np.matrix(values)
    diag = np.diag(np.sqrt(np.diagonal(cov)))
    return pd.DataFrame(cov, columns=names, index=names)

json_from_cov_df(df=)

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
