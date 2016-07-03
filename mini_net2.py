
from keras.models import Sequential
from keras.layers import Convolution2D, Dense, Dropout, Flatten, Activation, MaxPooling2D
from keras.callbacks import EarlyStopping, ModelCheckpoint

from keras.utils import np_utils

import numpy as np


def initialize_model():
    model = Sequential()
    model.add(Convolution2D(20, 5, 5, border_mode='valid', input_shape=(1, 40, 40)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Convolution2D(60, 5, 5))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(500))
    model.add(Activation('sigmoid'))
    model.add(Dropout(0.5))
    model.add(Dense(10))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])


    model.load_weights('weights.hdf5') 
    return model


def run_test(vector):
    model = initialize_model()

    testX = np.array(vector).reshape(40, 40)
    testX = testX.reshape(1, 1, 40, 40)
    testY = model.predict(testX)
    ans_val = np.argmax(testY)
    ans = [ans_val, float(testY[0][ans_val])]
    
    return ans
