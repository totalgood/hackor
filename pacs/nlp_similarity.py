import pandas as pd

import matplotlib
%matplotlib inline
np = pd.np
np.norm = np.linalg.norm
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split

pacs_scraped = pd.DataFrame.from_csv('public.raw_committees_scraped.csv')  # id
pacs = pd.DataFrame.from_csv('public.raw_committees.csv')  # no ID that I can find
candidates = pd.DataFrame.from_csv('public.raw_candidate_filings.csv')  # id_nmbr
print(pacs_scraped.info())
print(candidates.info())

df = pacs_scraped
names = df.index.values
corpus = [' '.join(str(f) for f in fields) for fields in
          zip(*[df[col] for col in df.columns if df[col].dtype == pd.np.dtype('O')])]
print(corpus[:3])
vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 1), stop_words='english')
tfidf = vectorizer.fit_transform(corpus)
print(dir(tfidf))
cov = tfidf * tfidf.T

