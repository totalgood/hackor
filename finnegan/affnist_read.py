""" a load and transform script:

This takes the affNIST dataset, a transformation of the original MNIST
dataset (via rotations, skews, and steps) to extend it to 2m+ entries.
The work on this was done by http://www.cs.toronto.edu/~tijmen/affNIST/

The parsing script came from StackOverflow at this link:
https://stackoverflow.com/questions/7008608/scipy-io-loadmat-nested-structures-i-e-dictionaries

The rest is by me (Cole Howard) to translate it into a dataset readable
by the Finnegan (http://uglyboxer.github.io/finnegan/) neural network.
"""

import numpy as np
import scipy.io as spio


def loadmat(filename):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)


def _check_keys(dict):
    '''
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries
    '''
    for key in dict:
        if isinstance(dict[key], spio.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict        


def _todict(matobj):
    '''
    A recursive function which constructs from matobjects nested dictionaries
    '''
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, spio.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict


if __name__ == '__main__':
    
    dataset = loadmat('training_batches/1.mat')

    ans_set = dataset['affNISTdata']['label_int']
    train_set = dataset['affNISTdata']['image'].transpose()


