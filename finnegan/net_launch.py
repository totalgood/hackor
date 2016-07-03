""" A launcher for the Finnegan neural net.
Author: Cole Howard

To allow for easily switching between datasets and hyperparameters.

"""
import csv
import dill
import numpy as np
from sklearn import datasets, utils

# from matplotlib import cm
# from matplotlib import pyplot as plt

from finnegan.network import Network


def run_scikit_digits(epochs=0, layers=0, neuron_count=0):
    """ Run Handwritten Digits dataset from Scikit-Learn.  Learning set is split
    into 70% for training, 15% for testing, and 15% for validation.

    Parameters
    ----------
    epochs : int
        Number of iterations of the the traininng loop for the whole dataset
    layers : int
        Number of layers (not counting the input layer, but does count output
        layer)
    neuron_count : list
        The number of neurons in each of the layers (in order), does not count
        the bias term

    Attributes
    ----------
    target_values : list
        The possible values for each training vector

    """

    # Imported from linear_neuron
    temp_digits = datasets.load_digits()
    digits = utils.resample(temp_digits.data, random_state=3)
    temp_answers = utils.resample(temp_digits.target, random_state=3)
    # images = utils.resample(temp_digits.images, random_state=0)
    num_of_training_vectors = 1250 
    answers, answers_to_test, validation_answers = temp_answers[:num_of_training_vectors], temp_answers[num_of_training_vectors:num_of_training_vectors+260], temp_answers[num_of_training_vectors+260:]
    training_set, testing_set, validation_set = digits[:num_of_training_vectors], digits[num_of_training_vectors:num_of_training_vectors+260], digits[num_of_training_vectors+260:]

    ###########
    # network.visualization(training_set[10], answers[10])
    # network.visualization(training_set[11], answers[11])
    # network.visualization(training_set[12], answers[12])

    network = Network(layers, neuron_count, training_set[0])
    network.train(training_set, answers, epochs)
    f = open('my_net.pickle', 'wb')
    # fr = open('my_net.pickle', 'rb')
    dill.dump(network, f)
    # network = pickle.load(fr)
    # fr.close()
    f.close()
    # guess_list = network.run_unseen(testing_set)
    return network.run_unseen(testing_set)
    # network.report_results(guess_list, answers_to_test)
    # valid_list = network.run_unseen(validation_set)
    # network.report_results(valid_list, validation_answers)


def run_mnist(epochs, layers, neuron_count):
    """ Run Mnist dataset and output a guess list on the Kaggle test_set

    Parameters
    ----------
    epochs : int
        Number of iterations of the the traininng loop for the whole dataset
    layers : int
        Number of layers (not counting the input layer, but does count output
        layer)
    neuron_count : list
        The number of neurons in each of the layers (in order), does not count
        the bias term

    Attributes
    ----------
    target_values : list
        The possible values for each training vector

    """

    with open('train.csv', 'r') as f:
        reader = csv.reader(f)
        t = list(reader)
        train = [[int(x) for x in y] for y in t[1:]]

    with open('test.csv', 'r') as f:
        reader = csv.reader(f)
        raw_nums = list(reader)
        test_set = [[int(x) for x in y] for y in raw_nums[1:]]

    ans_train = [x[0] for x in train]
    train_set = [x[1:] for x in train]
    ans_train.pop(0)
    train_set.pop(0)

    train_set = utils.resample(train_set, random_state=2)
    ans_train = utils.resample(ans_train, random_state=2)

    network = Network(layers, neuron_count, train_set[0])
    network.train(train_set, ans_train, epochs)

    # For validation purposes
    # guess_list = network.run_unseen(train_set[4000:4500])
    # network.report_results(guess_list, ans_train[4000:4500])
    # guess_list = network.run_unseen(train_set[4500:5000])
    # network.report_results(guess_list, ans_train[4500:5000])

    guess_list = network.run_unseen(test_set)
    with open('digits.txt', 'w') as d:
        for elem in guess_list:
            d.write(str(elem)+'\n')

if __name__ == '__main__':
    epochs = 250
    layers = 3
    layer_list = [36, 34, 10]
    run_scikit_digits(epochs, layers, layer_list)
    # run_mnist(epochs, layers, layer_list)

