from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from rest_framework.renderers import JSONRenderer
# from django.views.decorators.csrf import csrf_exempt

from models import Song_BOW
from predict_year.serializers import BOWSerializer
from predict import parse_data_predict

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

        The probability percentage is out of the seven decades that are available as choices. 
    """

    song_lyrics = request.body

    # Check request body to make sure it's at least 4 words or longer 
    text_list = song_lyrics.split()
    if len(text_list) < 4:
        detail = "your request body must be longer than three words"
        raise ParseError(detail=detail, code=400) 

    # check to make sure body doesn't contain numbers 
    for word in text_list: 
        if word.isdigit(): 
            detail = "your request must not contain numbers"
            print(detail)
            raise ParseError(detail=detail, code=400) 

    # send data to predict.py for stemming, dict conversion, and prediction
    parse_data_predict(song_lyrics)

    # grabs most recently created object from DB so you can access prediction 
    obj = Song_BOW.objects.all().order_by('-id')[0]

    # turns object into python dict so you can access it 
    serializer = BOWSerializer(obj)

    prediction = (serializer['year'].value) * 10
    confidence = serializer['confidence'].value

    # setting up object that is returned to user 
    response = {
                "predicted_decade": str(prediction)+'s',
                "prob_of_decade": confidence
                }
                

    json = JSONRenderer().render(response)

    return HttpResponse(json)




