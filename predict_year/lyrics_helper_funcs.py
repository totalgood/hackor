import pickle
from scipy.sparse import lil_matrix

def load_dict():
    with open('pickles/save_dict.p', 'rb') as f:
        dicty = pickle.load(f)
    return dicty

def convert_dict(a_dict):
    dicty = load_dict()

    new_dict = {}
    for word in a_dict.keys():
        try:
            new_dict[dicty[word]] = a_dict[word]
        except:
            print('word not in dictionary, skipped')
            
    return new_dict

def matrix_func(a_list):
    """take a list of dicts and return a sparse lil_matrix"""
    # make a matrix that matches the size of list of dicts 
    sparse_matrix = lil_matrix((len(a_list), 5000))

    # loop through each dict in list, and add that dicts values to idx of key in sparse matrix 
    for idx, a_dict in enumerate(a_list):

        for key in a_dict.keys(): 
            # subtracting 1 from the key because values in dict start at 1 
            sparse_matrix[idx, key - 1] = a_dict[key]
    
    return sparse_matrix