""" Accept an array representing a test sample, parse it and pass through
a pre-trained neural net then store results in a pre-existing database
"""
from guess.models import Drawing

from finnegan.img_handler import downsize
from mini_net2 import run_test
# from skimage.util import pad

# def padwithtens(vector, pad_width, iaxis, kwargs):
#     vector[:pad_width[0]] = 0
#     vector[-pad_width[1]:] = 0
#     return vector

def parse_to_test_sample(info):
    """  Takes the info retrieved from the script.js implementation on main
    page and parses it.  Data is run against existing neural net and then
    stores net's output and original data in PostgreSQL database.

    Attributes
    ----------
    orig_size : int
        The length of a side of the square html input canvas.
    train_data_size : int
        The length of a side of the square 2d array representing the training
        data.

    """

    orig_size = 174
    train_data_size = 40
    if info != "no info":

        # Split payload into a list of floats and discard the rgb values
        # Alpha channel is used a greyscale value (Every 4th entry from
        # the sketch.js output)

        temp_array = info.split(',')
        orig_img = [float(x) for x in temp_array[3::4]]
        img_array = [float(x)/255 for x in temp_array[3::4]]

        # Resize the image to match the size of the network's training
        # data

        small_image = downsize(img_array, orig_size, train_data_size)
        small_image_list = small_image.flatten().tolist()

        # Pass it through the pre-trainedd network and retrieve a guess
        # and confidence

        net_guess = run_test(small_image)
        val_guess = net_guess[0]
        net_confidence = net_guess[1] * 100


    else:
        img_array = None

    Drawing.objects.create(values_array=orig_img,
                           guess=val_guess,
                           confidence=net_confidence,
                           tiny_array=small_image_list,
                           correct=False)
