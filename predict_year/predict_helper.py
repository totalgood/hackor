import gensim
import pickle
from sklearn.externals import joblib
from scipy.sparse import lil_matrix
from word_stemmer import lyrics_to_bow

def stemming_dict(data):
    stemmed_data = lyrics_to_bow(data)
    return stemmed_data

def dict_number_keys(a_dict):
    """map BOW dict keys to number values of words in corpus"""
    with open('pickles/save_dict.p', 'rb') as f:
        dicty = pickle.load(f)
        new_dict = {}
        for word in a_dict.keys():
            try:
                new_dict[dicty[word]] = a_dict[word]
            except:
                # word not in corpus word dict
                continue
    return new_dict

def tfidf_dict(num_dict):
    """turn dict into a dict of word_keys: tfidf_scores"""
    tfidf = gensim.models.TfidfModel.load("pickles/full_tfidf_model.tfidf")
    song_tfidf = tfidf[num_dict.items()]

    tfidf_dict = {}
    for key, value in song_tfidf:
        tfidf_dict[key] = value

    return tfidf_dict

def make_lil_matrix(tfidf_dict):
    """create a lil_matrix out of tfidf_dict so it can be made dense during training"""

    # making a list with a dict as the only element to mirror the training process used in model
    a_list = [tfidf_dict]
    sparse_matrix = lil_matrix((len(a_list), 5000))

    # loop through each dict in list, and add that dicts values to idx of key in sparse matrix
    for idx, a_dict in enumerate(a_list):

        for key in a_dict.keys():
            # subtracting 1 from the key because values in dict start at 1
            sparse_matrix[idx, key - 1] = a_dict[key]
    return sparse_matrix

def predict_decade(a_matrix):
    """load model and get year prediciton and probability score"""

    with open('pickles/NB_pickles.pkl', 'rb') as fo:
        clf = joblib.load(fo)

    prediction = clf.predict(a_matrix[0].toarray())

    # need to add 5 because 50's are zero index in model
    year = prediction[0] + 5

    # gets probability scores for each decade
    decade_probabilities = clf.predict_proba(a_matrix[0].toarray())

    # creating a dict of the prob of each decade. Adding 5 because 50s zero index
    probability_scores = [((idx+5), score) for idx, score in enumerate(decade_probabilities[0])]

    prob_dict = {}
    for item in probability_scores:
        prob_dict[str(item[0])] = str(item[1])

    song_obj = {
               'year': year,
               'confidence': decade_probabilities[0][prediction][0],
               'prob_decades': prob_dict
                }

    return song_obj

