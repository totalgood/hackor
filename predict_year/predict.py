import gensim
import pickle
from sklearn.externals import joblib

from lyrics_helper_funcs import convert_dict, matrix_func

# imports stemming script used on all lyrics in model 
from word_stemmer import lyrics_to_bow
from models import Song_BOW


def parse_data_predict(data):
    parsed_data = lyrics_to_bow(data)
    
    # converts parsed_data dict to a dict with numeric key values that match training             
    new_test = convert_dict(parsed_data)

    # turn dict into a dict of word_keys: tfidf_scores 
    tfidf = gensim.models.TfidfModel.load("pickles/full_tfidf_model.tfidf")
    song_tfidf = tfidf[new_test.items()]

    tfidf_dict = {}
    for key, value in song_tfidf:
        tfidf_dict[key] = value

    # create a lil_matrix out of tfidf_dict so it can be made dense during training 
    dense = matrix_func([tfidf_dict])
    
    # load model and get year prediciton and probability score 
    with open('pickles/NB_pickles.pkl', 'rb') as fo:
        clf = joblib.load(fo)
 
    prediction = clf.predict(dense[0].toarray())

    # need to add 5 because 50's are zero index in model
    year = prediction[0] + 5 

    # gets probability scores for each decade 
    decade_probabilities = clf.predict_proba(dense[0].toarray())

    # creating a dict of the prob of each decade. Adding 5 because 50s zero index 
    probability_scores = [((idx+5), score) for idx, score in enumerate(decade_probabilities[0])]

    prob_dict = {}
    for item in probability_scores:
        prob_dict[str(item[0])] = str(item[1])

    Song_BOW.objects.create(
                            bow=tfidf_dict,
                            year=year,
                            confidence=decade_probabilities[0][prediction], 
                            prob_decades=prob_dict
                            )










