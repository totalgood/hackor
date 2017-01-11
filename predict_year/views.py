from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import status
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
# from django.views.decorators.csrf import csrf_exempt

import predict_helper

# @csrf_exempt
@api_view(['POST'])
def lyrics_prediction(request):
    """ 
        Send request to API using POST with a string in the body of the request. 
        This string must be longer than three words and must not contain any digits. 
        After receiving the POST request the API will parse the lyrics and run a Naive Bayes 
        prediction model in an attempt to predict which the decade the song lyrics are from. 

        Example: 
        post('/predict/',song_lyrics_text, 'application/json') 
        reponse 200: {predicted_decade: '90s', prob_of_decade: '0.273208'}

        The prob_of_decade is based on the seven decades that are available as choices. 
    """

    song_lyrics = request.body

    text_list = song_lyrics.split()

    # Check request body to make sure it's at least 4 words or longer
    if len(text_list) < 4:
        detail = "your request body must be longer than three words"
        return Response(detail, status=status.HTTP_400_BAD_REQUEST)

    # check to make sure body doesn't contain numbers
    for word in text_list:
        if word.isdigit():
            detail = "your request must not contain numbers"
            return Response(detail, status=status.HTTP_400_BAD_REQUEST)

    # stem song lyrics and return dict with word counts
    stemmed_data = predict_helper.stemming_dict(song_lyrics)

    # convert stemmed_data to a dict where keys are nums that map to words in corpus
    num_dict = predict_helper.dict_number_keys(stemmed_data)

    # convert num dict values to their tfidf scores
    tfidf_dict = predict_helper.tfidf_dict(num_dict)

    # convert tfidf_dict to lil_matrix so it can be made dense during prediction
    a_matrix = predict_helper.make_lil_matrix(tfidf_dict)

    # make prediction and return object with prediciton and probability of decade
    song_obj = predict_helper.predict_decade(a_matrix)

    # changes value of predicted decade to output format
    prediction = (song_obj['year']) * 10

    if prediction == 100:
        prediction = 2000
    elif prediction == 110:
        prediction = 2010

    confidence = song_obj['confidence']

    # set up object that is returned to user
    response = {
                "predicted_decade": str(prediction)+'s',
                "prob_of_decade": confidence
                }

    json = JSONRenderer().render(response)

    return HttpResponse(json)




