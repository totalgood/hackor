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

pacs_scraped = pd.DataFrame.from_csv('data/public.raw_committees_scraped.csv')  # id
pacs = pd.DataFrame.from_csv('data/public.raw_committees.csv')  # no ID that I can find
print(pacs_scraped.info())
# print(candidates.info())

df = pacs_scraped
names = df.index.values
corpus = [' '.join(str(f) for f in fields if (not isinstance(f, (float, int, datetime, date, np.int_, np.float_)) and not f in (None, np.nan)))
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
# rows should be documents, columns should be "words"
vectors = vectorizer.fit(corpus)
tfidf = vectors.transform(corpus)
tfidf_df = pd.DataFrame(tfidf.todense(), index=names)
cov = tfidf * tfidf.T
cov_df = pd.DataFrame(cov.todense(), columns=names, index=names)


def graph_from_cov_df(df=cov_df, threshold=.5, gain=20., n=400):
    """Compose pair of lists of dicts (nodes, edges) for the graph described by a DataFrame"""
    nodes = [{'group': 1, "name": name} for name in df.index.values][:n]
    edges = []
    for i, (row_name, row) in enumerate(df.iterrows()):
        for j, value in enumerate(row.values):
            if i > j and value * gain > threshold and i < n and j < n:
                edges += [{'source': i, 'target': j, 'value': gain * value}]
    return nodes, edges


def json_from_cov_df(df=cov_df, threshold=.5, gain=10., n=400, indent=1):
    """Produce a json string describing the graph (list of edges) from a square auto-correlation/covariance matrix

       { "nodes": [{"group": 1, "name": "the"},
                {"group": 1, "name": "and"},
                {"group": 1, "name": "our"},
                {"group": 2, "name": "that"},...
         "links": [{"source": 0, "target": 0, "value": 2.637520131294177},
                   {"source": 0, "target": 1, "value": 1.343999676850537}, ...
    """
    nodes, edges = graph_from_cov_df(df=df, threshold=threshold, gain=gain, n=n)
    return json.dumps([{'nodes': nodes, 'links': edges}], indent=indent)


def main(filename='nlp_similarity_graph.json', verbosity=1):
    js = json_from_cov_df()
    if verbosity:
        print(js[:1000] + '\n...\n' + js[-1000:])
    with open(filename, 'w') as f:
        f.write(js)


if __name__ == '__main__':
    main()
