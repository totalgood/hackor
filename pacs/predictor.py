#!python manage.py shell_plus <
import numpy as np
np.norm = np.linalg.norm

import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split



from pacs.models import RawCommittees

pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SGDClassifier()),
])


def label_from_name(names=np.array(RawCommittees.objects.values_list('committee_name', flat=True)),
                    labels=RawCommittees.objects.values_list('committee_type', 'committee_subtype'),
                    alpha=1e-5,
                    penalty='l1',
                    verbosity=0,
                    classifier=None,
                   ):
    """Train or excercise a classifier that predicts a committee type, subtype (label) from its name

    Args:
      names (array of str): the committee names (space-delimitted words with a few words)
      labels (array of 2-tuple of str): the committee_type and subtype, Nones/NaNs/floats are stringified
      alpha (float): learning rate (sklearn TFIDF classifier examples use 1e-5 to 1e-6)
            default: 1e-5
      penalty: 'none', 'l2', 'l1', or 'elasticnet'  # regularization penalty on the feature weights

    Returns:
      On first call or if classier arg is None returns a trained SVM classifier instance
      It called with a str then returns the type and subtype predicted for that PAC name
    """
    name = names if isinstance(names, basestring) else None
    self = label_from_name
    if classifier is not None:
        self.classifier = classifier
    if self.classifier is None or self.classifier is True:
        vectorizer = CountVectorizer(min_df=1)
        self.names = (names if isinstance(names, (list, np.ndarray))
                      else RawCommittees.objects.values_list('committee_name', flat=True))

        self.labels = np.array(list(labels or RawCommittees.objects.values_list('committee_type', 'committee_subtype')))
        self.labels = np.array([str(lbl) for lbl in self.labels])
        word_bag = vectorizer.fit_transform(self.names)
        print(word_bag)
        self.tfidf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.names)
        words = self.tfidf.get_feature_names()
        print(self.tfidf)
        try:
            train_tfidf, test_tfidf, train_labels, test_labels = train_test_split(self.tfidf_matrix, self.labels, test_size=.25)
        except:
            import ipdb; ipdb.set_trace()
        # alpha: learning rate (default 1e-4, but other TFIDF classifier examples use 1e-5 to 1e-6)
        # penalty: 'none', 'l2', 'l1', or 'elasticnet'  # regularization penalty on the feature weights
        self.classifier = SGDClassifier(alpha=alpha, penalty=penalty)
        pac_type_tuples = RawCommittees.objects.values_list('committee_type', 'committee_subtype')
        pac_types = [', '.join(str(s) for s in pt) for pt in pac_type_tuples]
        self.matrix = self.classifier.fit(self.tfidf, self.labels)
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
