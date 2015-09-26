#!python manage.py shell_plus <
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline

from pacs.models import RawCommittees

pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SGDClassifier()),
])

pac_names = RawCommittees.objects.values_list('committee_name', flat=True)
vectorizer = CountVectorizer(min_df=1)
word_bag = vectorizer.fit_transform(pac_names)
tfidf_xf = TfidfTransformer()
tfidf = tfidf_xf.fit_transform(word_bag)
# alpha: learning rate (default 1e-4, but other TFIDF classifier examples use 1e-5 to 1e-6)
# penalty: ‘none’, ‘l2’, ‘l1’, or ‘elasticnet’  # regularization penalty on the feature weights
clf_xf = SGDClassifier(alpha=1e-5, penalty='l1')
pac_type_tuples = RawCommittees.objects.values_list('committee_type', 'committee_subtype')
pac_types = [', '.join(str(s) for s in pt) for pt in pac_type_tuples]
clf = clf_xf.fit_transform(tfidf, pac_types)
clf_xf.score(tfidf, pac_types)
# > 98% recall (accuracy on training set)
