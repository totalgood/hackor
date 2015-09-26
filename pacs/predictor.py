#!python manage.py shell_plus <
import numpy as np
np.norm = np.linalg.norm

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


def label_from_name(names=RawCommittees.objects.values_list('committee_name', flat=True),
                    labels=RawCommittees.objects.values_list('committee_type', 'committee_subtype'),
                    alpha=1e-5,
                    penalty='l1',
                    verbosity=0,
                    classifier=None,
                   ):
    """Train or excercise a classifier that predicts a committee type, subtype (label) from its name"""
    name = names if isinstance(names, basestring) else None
    self = label_from_name
    if classifier is not None:
        self.classifier = classifier
    if self.classifier is None or self.classifier is True:
        vectorizer = CountVectorizer(min_df=1)
        self.names = (names if isinstance(names, (list, np.ndarray))
                      else RawCommittees.objects.values_list('committee_name', flat=True))
        labels = labels or RawCommittees.objects.values_list('committee_type', 'committee_subtype')
        word_bag = vectorizer.fit_transform(self.names)
        self.tfidf = TfidfTransformer()
        self.tfidf.fit(word_bag)
        # alpha: learning rate (default 1e-4, but other TFIDF classifier examples use 1e-5 to 1e-6)
        # penalty: 'none', 'l2', 'l1', or 'elasticnet'  # regularization penalty on the feature weights
        self.classifier = SGDClassifier(alpha=alpha, penalty=penalty)
        pac_type_tuples = RawCommittees.objects.values_list('committee_type', 'committee_subtype')
        pac_types = [', '.join(str(s) for s in pt) for pt in pac_type_tuples]
        self.matrix = self.classifier.fit(self.tfidf, np.array(str(lbl) for lbl in labels))
        if verbosity > 0:
            print(self.classifier.score(self.tfidf, pac_types))
            # Typically > 98% recall (accuracy on training set)
        return self.classifier
    if isinstance(name, basestring):
        vec = self.tfidf.transform(name)
        predicted_label = self.classifier.predict(vec)
        print(predicted_label)
        return predicted_label
    return self.classifier
label_from_name.tfidf = None
label_from_name.names = None
label_from_name.classifier = None


def similarity(name1, name2):
    label_from_name()
    tfidf = label_from_name.tfidf
    vec1, vec2 = tfidf.transform([name1, name2])
    return np.norm(vec1) * np.norm(vec2.norm) / np.dot(vec1, vec2)
