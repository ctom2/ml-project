import numpy as np
import math
from classifiers import Classifiers
import random
import copy
import setter

# Class App contains all functions needed for the learning based on the values from csv file and calculating the predictions

class App:
    # class constructor
    def __init__(self, setter):
        self.training_data_array = []    # training data (first 67% of the original dataset) = first part
        self.training_results_array = []     # results of the training data
        self.validation_data_array = []      # validation data (remaining 33% of the original dataset) = second part
        self.validation_results_array = []   # results of the validation data

        self.data_columns = ['radius', 'texture', 'perimeter', 'area', 'smoothness', 'compactness', 
                             'concavity', 'concave points', 'symetry', 'fractal dimension']

        self.get_data(setter.dataset)
        self.split_data()
        self.train_on_data()

        setter.pick_algo()

        if setter.algo == 'kNN':
            self.main_classifier = self.classifiers.knn_classifier
        elif setter.algo == 'SVC':
            self.main_classifier = self.classifiers.svc_classifier
        elif setter.algo == 'GaussianNB':
            self.main_classifier = self.classifiers.gauss_classifier
        elif setter.algo == 'RandomForest':
            self.main_classifier = self.classifiers.forest_classifier

    # reads data from dataset, saves the result values and deletes first two columns
    def get_data(self, dataset):
        self.data_array = np.genfromtxt(dataset, delimiter=',', 
            dtype='float64, U1, float64, float64, float64, float64, float64, float64, float64, float64, float64, float64')
        tmp = np.array([list(elem) for elem in self.data_array])

        tmp = np.delete(tmp, 0, 1)
        self.results_array = tmp[:,0]
        tmp = np.delete(tmp, 0, 1)
        self.data_array = tmp.astype(np.float)

    # splits data into two datasets, first part is intended for learning and second part is intended for validation
    # and choosing the best k-value used in following functions
    def split_data(self, training_size = 0.67):
        training_length = math.ceil(len(self.data_array) * training_size)
        for i in range(training_length):
            self.training_data_array.append(self.data_array[i])
            self.training_results_array.append(self.results_array[i])

        for i in range(len(self.data_array) - training_length):
            self.validation_data_array.append(self.data_array[i + training_length])
            self.validation_results_array.append(self.results_array[i + training_length])

        self.training_data_array = np.array(self.training_data_array)
        self.training_results_array = np.array(self.training_results_array)
        self.validation_data_array = np.array(self.validation_data_array)
        self.validation_results_array = np.array(self.validation_results_array)

    def train_on_data(self):
        self.classifiers = Classifiers(self.training_data_array, self.training_results_array, self.validation_data_array, self.validation_results_array)
        self.classifiers.train_on_values_knn()
        self.classifiers.train_on_values_svc()
        self.classifiers.train_on_values_gauss()
        self.classifiers.train_on_values_forest()
        print('--------')
        print('kNN\naccuracy score =', self.classifiers.knn_classifier.score(self.validation_data_array, self.validation_results_array), '\n--------')
        print('SVC\naccuracy score =', self.classifiers.svc_classifier.score(self.validation_data_array, self.validation_results_array), '\n--------')
        print('GaussianNB\naccuracy score =', self.classifiers.gauss_classifier.score(self.validation_data_array, self.validation_results_array), '\n--------')
        print('RandomForest\naccuracy score =', self.classifiers.forest_classifier.score(self.validation_data_array, self.validation_results_array), '\n--------')

    # predicts the result of entered data
    def predict(self, entries):
        data = []
        for i in range(len(entries)):
            data.append(entries[i].get())

        data = np.array(data)
        data = data.reshape(1, -1)
        data = data.astype(np.float64)

        return self.main_classifier.predict(data)