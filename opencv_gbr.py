#!/usr/bin/env python

import cv2

import pandas as pd
import numpy as np

from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV


def shuffle_data(df):
    return df.reindex(np.random.permutation(df.index))


class OpenCVGradientBoostingClassifier:
    def __init__(self, **kwargs):
        self.gbt = cv2.GBTrees()
        self.params = {
            'loss_function_type': cv2.GBTREES_DEVIANCE_LOSS,
            'subsample_portion': 0.5,
            'max_depth': 6,
            'weak_count': 250
        }
        self.params.update(kwargs)

    def fit(self, x, y):
        self.gbt.train(x, cv2.CV_ROW_SAMPLE, y, params=self.params)
        return self

    def predict(self, x):
        return self.__predict_impl(x, -1)

    def predict_probability(self, x):
        a = self.__predict_impl(x, 0)
        b = self.__predict_impl(x, 1)
        return np.exp(a) / (np.exp(a) + np.exp(b))

    def scores(self, x, y, error_function, step=1):
        res = []
        for iterations in range(step, self.params['weak_count'] + step, step):
            predicted = self.__predict_impl(x, k=-1, slice=(0, iterations))
            res.append((iterations, error_function(y, predicted)))
        return res

    def __predict_impl(self, x, k, slice=None):
        res = np.empty(len(x), dtype=np.float32)
        for i in range(0, len(x)):
            res[i] = self.gbt.predict(x[i], k=k, slice=slice)
        return res

    def get_params(self, deep=True):
        return self.params

    def set_params(self, **parameters):
        self.params.update(parameters)


def main():
    with open('spambase.names', 'r') as inp:
        column_names = inp.read().split("\n")
    data = pd.read_csv("spambase.data", names=column_names)
    data = shuffle_data(data)

    x = data.drop('spam', 1).fillna(0).as_matrix().astype(np.float32)
    y = data.spam.values.astype(np.float32)

    x_train, x_test, \
        y_train, y_test = train_test_split(x, y, test_size=0.3)


    tuned_parameters = [
        { 'weak_count': [300, 500, 100],
          'max_depth': [4, 6, 10]
        }
    ]

    clf = GridSearchCV(OpenCVGradientBoostingClassifier(), tuned_parameters, cv=3, scoring='f1', verbose=2, refit=False)
    clf.fit(x_train, y_train)

    for params, mean_score, scores in clf.grid_scores_:
        print "%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() / 2, params)

if __name__ == "__main__":
    main()