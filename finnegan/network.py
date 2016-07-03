""" Author: Cole Howard

An extinsible neural net designed to explore Neural Network Architecture via
extensive visualizations.

"""

import numpy as np
from sklearn.preprocessing import normalize

from finnegan.layer import Layer


class Network:
    """ A multi layer neural net with backpropogation.

    Parameters
    ----------
    layers : int
        Number of layers to use in the network.
    neuron_count : list
        A list of integers that represent the number of neurons present in each
        hidden layer.  (Size of input/output layers are dictated by dataset)
    vector : list
        Example vector to get size of initial input

    Attributes
    ----------
    possible : list
        A list of possible output values

    """

    def __init__(self, layers, neuron_count, vector):
        self.num_layers = layers
        self.neuron_count = neuron_count
        self.possible = [x for x in range(10)]
        self.layers = [Layer(self.neuron_count[x], self.neuron_count[x-1]) if
                       x > 0 else Layer(self.neuron_count[x], len(vector))
                       for x in range(self.num_layers)]

    def _pass_through_net(self, vector, dropout=True):
        """ Sends a vector into the net

        Parameters
        ----------
        vector : numpy array
            A numpy array representing a training input (without the target)
        dropout : bool
            Whether or not you should perform random dropout in the pass through
            the net.  (Set False for the tesing set vectors)

        Returns
        -------
        numpy array
            Output of the last layer in the chain

        """
        for x, _ in enumerate(self.layers):
            vector = self.layers[x]._vector_pass(vector, dropout)
        return vector

    def _softmax(self, w, t=1.0):
        """Author: Jeremy M. Stober, edits by Martin Thoma
        Program: softmax.py
        Date: Wednesday, February 29 2012 and July 31 2014
        Description: Simple softmax function.
        Calculate the softmax of a list of numbers w.

        Parameters
        ----------
        w : list of numbers
        t : float

        Return
        ------
        a list of the same length as w of non-negative numbers

        Examples
        --------
        >>> softmax([0.1, 0.2])
        array([ 0.47502081,  0.52497919])
        >>> softmax([-0.1, 0.2])
        array([ 0.42555748,  0.57444252])
        >>> softmax([0.9, -10])
        array([  9.99981542e-01,   1.84578933e-05])
        >>> softmax([0, 10])
        array([  4.53978687e-05,   9.99954602e-01])

        """
        e_x = np.exp(w - np.max(w))
        out = e_x / e_x.sum()
        return out

    def _backprop(self, guess_vector, target_vector):
        """ Takes the output of the net and initiates the backpropogation

        In output layer:
          generate error matrix [(out * (1-out) * (Target-out)) for each neuron]
          update weights matrix [[+= l_rate * error_entry * input TO that
          amount] for each neuron ]

        In hidden layer
          generate error matrix [out * (1-out) * dotproduct(entry in n+1 error
          matrix, n+1 weight of that entry)] update weights matrix [[+= l_rate
          for each weight] for each neuron]

        Parameters
        ----------
        guess_vector : numpy array
            The output from the last layer during a training pass
        target_vector : list
            List of expected values

        Attributes
        ----------


        Returns
        -------
        True
            As evidence of execution

        """
        backwards_layer_list = list(reversed(self.layers))
        for i, layer in enumerate(backwards_layer_list):
            if i == 0:
                hidden = False
                layer_ahead = None
            else:
                hidden = True
                layer_ahead = backwards_layer_list[i-1]
            if layer._layer_level_backprop(guess_vector, layer_ahead, target_vector, hidden):
                continue
            else:
                print("Backprop failed on layer: " + str(i))
        for layer in self.layers:
            layer._update_weights()
        # for layer in self.layers:        
        #     layer.error_matrix = []
        return True

    def train(self, dataset, answers, epochs):
        """ Runs the training dataset through the network a given number of
        times.

        Parameters
        ----------
        dataset : Numpy nested array
            The collection of training data (vectors and the associated target
            value)
        answers : numpy array
            The array of correct answers to associate with each training
            vector
        epochs : int
            Number of times to run the training set through the net

        """
        for x in range(epochs):
            for vector, target in zip(dataset, answers):
                target_vector = [0 if x != target else 1 for x in self.possible]
                vector = np.array(vector).reshape(1, -1)
                vector = vector.astype(float)
                vector = normalize(vector, copy=False)[0]
                y = self._pass_through_net(vector, dropout=False)
                z = self._softmax(y)
                self._backprop(z, target_vector)

            amt_off = (sum((self.layers[self.num_layers-1].error)**2))/10
            print(amt_off)
            if amt_off < .00055:
                break

    def run_unseen(self, test_set):
        """ Makes guesses on the unseen data, and switches over the test
        answers to validation set if the bool is True

        For each vector in the collection, each neuron in turn will either
        fire or not.  If a vector fires, it is collected as a possible
        correct guess.  Not firing is collected as well, in case
        there an no good guesses at all.  The method will choose the
        vector with the highest dot product, from either the fired list
        or the dud list.

        Parameters
        ----------
        test_set : list
            List of numpy arrays representing the unseen vectors

        Returns
        -------
        list
            a list of ints (the guesses for each vector)
        """
        guess_list = []
        for vector in test_set:
            vector = np.array(vector).reshape(1, -1)
            vector = vector.astype(float)
            temp = self._pass_through_net(normalize(vector, copy=False)[0],
                                          dropout=False)
            guess_list.append((temp.argmax(), max(temp)))
        return guess_list

    def report_results(self, guess_list, answers):
        """ Reports results of guesses on unseen set

        Parameters
        ----------
        guess_list : list
        answers : list

        """

        successes = 0
        for idx, item in enumerate(guess_list):
            if answers[idx] == item[0]:
                successes += 1

        a = "Successes: {}  Out of total: {}".format(successes,
              len(guess_list))
        b = "For a success rate of: {}".format(successes/len(guess_list))
        print(a)
        print(b)
        return a + '\n' + b


if __name__ == '__main__':
    print("Please use net_launch.py")
