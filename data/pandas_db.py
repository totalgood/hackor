import json

import pandas as pd

import matplotlib
np = pd.np
np.norm = np.linalg.norm
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split


# pacs = pd.DataFrame.from_csv('data/public.raw_committees.csv')  # no ID that I can find
#candidates = pd.DataFrame.from_csv('data/public.raw_candidate_filings.csv')  # id_nmbr
# print(pacs_scraped.info())
# print(candidates.info())
# df = pacs_scraped


def corpus_from_table(df=pd.DataFrame.from_csv('data/public.raw_committees_scraped.csv'),
                      verbosity=None):
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


def json_from_cov_df(df=cov_from_corpus(corpus_from_table()), threshold=.5):
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
    corpus = corpus_from_table(verbosity=1)
    print(corpus)