from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.db.models import Sum

from guess.models import Drawing, Stats
from guess.predict import parse_to_test_sample

import logging


logging.basicConfig(filename='badness.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def home_page(request):
    return render(request, 'home.html')


@require_POST
def parse_data(request):
    """ As a request comes from the home page via POST, parse the canvas
    image, downsize it to match the dims of the training data, and then
    pass it to the pre-trained neural network for it make a prediction.

    The results of the prediction (value and confidence), as well as the
    array representations of the images themselves are stored in the
    model, and hence the PostgresQL database.

    """

    try:
        info = request.POST.get('payload', 'no info')
        parse_to_test_sample(info)
        return HttpResponse()
    except:
        logger.exception('New way')
        return render(request, 'home.html')


def show_data(request):
    """ Sends a render of image as drawn and the network's guess and
    confidence via the report template.

    Attributes
    ----------
    drawing_obj : Drawing model instance
      The last line from the database (specifically the most recent entry).

    """
    try:
        drawing_obj = Drawing.objects.order_by('-id').first()
    except:
        logger.exception('No model.')
        return HttpResponse("Oops.  Something went wrong.")
    if drawing_obj.confidence < 85:
        return render(request, 'messing.html', {'drawing_obj': drawing_obj})
    else:
        return render(request, 'report.html', {'drawing_obj': drawing_obj})


@require_POST
def valid_info(request):
    """ Stores the users validation (or dis-validation) of the network's
    guess in the database along with what the user intended it to be, in the
    case of an incorrect guess.

    """
    obj = Drawing.objects.all().order_by('-id')[0]

    if request.POST["valid"] == "correct":
        obj.correct = True
        obj.save()
        stat = Stats.objects.get(digit=obj.guess)
        stat.correctly_guessed += 1
        stat.save()
    else:
        obj.correct = False
        obj.actual = request.POST["actual"]
        obj.save()
        fail_stat = Stats.objects.get(digit=obj.actual)
        fail_stat.incorrectly_guessed += 1
        fail_stat.save()

    return redirect('/uglyboxer/') 

def stats_work(request):
    """ Work out statistics for results """

    digs = Stats.objects.all().order_by('digit')
    tot_correct = digs.aggregate(Sum('correctly_guessed'))
    tot_inc = digs.aggregate(Sum('incorrectly_guessed'))
    payload_digits = []
    for num in digs:
        temp = {'number': num.digit, 'correct': num.correctly_guessed,
                'incorrect': num.incorrectly_guessed}
        payload_digits.append(temp)
    return render(request, 'stats_view.html', {"digits": payload_digits,
                        "tot_correct": tot_correct['correctly_guessed__sum'],
                        "tot_inc": tot_inc['incorrectly_guessed__sum']})


def about(request):
    return redirect("http://uglyboxer.github.io/capstone/")


def contact(request):
    return redirect("https://github.com/uglyboxer")
