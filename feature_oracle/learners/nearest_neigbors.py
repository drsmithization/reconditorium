#!/usr/bin/env python

from learner import BaseLearner
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier


class NearestNeighbor(BaseLearner):
    def __init__(self, n_folds):
        super(NearestNeighbor, self).__init__(n_folds)

    def learn(self, x, y):
        knn = KNeighborsClassifier()
        return knn.fit(x, y)

    def err(self, y, predictions):
        return accuracy_score(y, predictions)