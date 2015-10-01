#!python manage.py shell_plus <
import pandas as pd
np = pd.np
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


def debug():
    import ipdb
    ipdb.set_trace()


class PACClassifier(SGDClassifier):

    def __init__(self,
                 names=np.array(RawCommittees.objects.values_list('committee_name', flat=True)),
                 labels=RawCommittees.objects.values_list('committee_type', 'committee_subtype'),
                 alpha=1e-5,
                 penalty='l1',
                 verbosity=1,
                 ):
        """Train a classifier that predicts a committee type, subtype (label) from its name

        Args:
          names (array of str): the committee names (space-delimitted words with a few words)
          labels (array of 2-tuple of str): the committee_type and subtype, Nones/NaNs/floats are stringified
          alpha (float): learning rate (sklearn TFIDF classifier examples use 1e-5 to 1e-6)
                default: 1e-5
          penalty: 'none', 'l2', 'l1', or 'elasticnet'  # regularization penalty on the feature weights

        Returns:
          SGDClassifier: Trained SVM classifier instance
        """
        super(PACClassifier, self).__init__(alpha=alpha, penalty=penalty)
        if verbosity is not None:
            self.verbosity = verbosity
            # vectorizer = CountVectorizer(min_df=1)
        # word_bag = vectorizer.fit_transform(self.names)
        # print(word_bag)
        self.names = (names if isinstance(names, (list, np.ndarray))
                      else RawCommittees.objects.values_list('committee_name', flat=True))

        self.pac_type_tuples = RawCommittees.objects.values_list('committee_type', 'committee_subtype')
        self.labels = np.array(list(labels or self.pac_type_tuples))
        # self.labels = [', '.join(str(s) for s in pt) for pt in self.pac_type_tuples]
        self.labels = np.array([str(lbl) for lbl in self.labels])
        self.label_set = sorted(np.unique(self.labels))
        self.label_dict = dict(list(zip(self.label_set, range(len(self.label_set)))))
        self.label_ints = np.array([self.label_dict[label] for label in self.labels])
        if self.verbosity > 1:
            print(pd.Series(self.labels))
        if self.verbosity > 0:
            print(np.unique(self.labels))

        self.tfidf = TfidfVectorizer(analyzer='word', ngram_range=(1, 1), stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.names)
        if verbosity > 1:
            print(self.tfidf.get_feature_names())
        self.train_tfidf, self.test_tfidf, self.train_labels, self.test_labels = train_test_split(
            self.tfidf_matrix, self.label_ints, test_size=.25)
        # alpha: learning rate (default 1e-4, but other TFIDF classifier examples use 1e-5 to 1e-6)
        # penalty: 'none', 'l2', 'l1', or 'elasticnet'  # regularization penalty on the feature weights
        self.svn_matrix = self.fit(self.train_tfidf, self.train_labels)
        if verbosity > 0:
            print(self.score(self.train_tfidf, self.train_labels))
            # Typically > 98% recall (accuracy on training set)

    def predict_pac_type(self, name):
        name = str(name)
        vec = self.tfidf.transform(name)
        predicted_label = self.predict(vec)
        print(predicted_label)
        return predicted_label

    def similarity(self, name1, name2):
        # tfidf is already normalized, so no need to divide by the norm of each vector?
        vec1, vec2 = self.tfidf.transform(np.array([name1, name2]))
        # cosine distance between two tfidf vectors
        return vec1.dot(vec2.T)[0, 0]

    def similarity_matrix(self):
        return self.tfidf_matrix * self.tfidf_matrix.T
