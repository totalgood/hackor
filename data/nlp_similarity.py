import re
import pandas as pd
np = pd.np
np.norm = np.linalg.norm
from datetime import datetime, date

import matplotlib
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split

pacs_scraped = pd.DataFrame.from_csv('data/public.raw_committees_scraped.csv')  # id
pacs = pd.DataFrame.from_csv('data/public.raw_committees.csv')  # no ID that I can find
print(pacs_scraped.info())
print(candidates.info())

df = pacs_scraped
names = df.index.values
corpus = [' '.join(str(f) for f in fields if (not isinstance(f, (float, int, datetime, date, np._int, np._float)) and not f in (None, np.nan)))
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
print(dir(tfidf))
cov = tfidf * tfidf.T
cov_df = pd.DataFrame(cov.todense(), columns=names, index=names)
