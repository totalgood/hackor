import sklearn
from sklearn.feature_extraction.text import CountVectorizer
rawcom = RawCommittees.objects.all()[0]
rawcom.committee_name
pac_names = RawCommittee.objects.values('committee_name')
pac_names = RawCommittee.objects.values('committee_name')
pac_names = RawCommittees.objects.values('committee_name')
len(pac_names)
pac_names
pac_names = RawCommittees.objects.values_list('committee_name')
pac_names
pac_names = RawCommittees.objects.values_list('committee_name', flat=True)
vectorizer = CountVectorizer(min_df=1)
word_bag = vectorizer.fit_transform(pack_names)
word_bag = vectorizer.fit_transform(pac_names)
from sklearn.feature_extraction.text import TfidfTransformer
tfidf_xf = TfidfTransformer()
word_bag
dir(word_bag)
word_bag.toarray()
tfidf = tfidf_xf.fit_transform(word_bag)
tfidf
%paste
clf = SGDClassifier()
clf_xf = SGDClassifier()
clf = clf_xf.fit_transform(tfidf)
clf = clf_xf.fit_transform(tfidf, alpha=3e-6, penalty='l1')
clf = clf_xf.fit_transform(tfidf, alpha=3e-6)
clf = clf_xf.fit_transform??
rawcom.committee_type
rawcom.committee_subtype
who
history
pac_type = RawCommittees.objects.values_list('committee_type', 'committee_subtype')
pac_types = [', '.join(pt) for pt in pack_type]
pac_types = [', '.join(pt) for pt in pac_type]
pac_types = [', '.join(str(s) for s in pt) for pt in pac_type]
pac_types
clf = clf_xf.fit_transform(tfidf, pac_types)
