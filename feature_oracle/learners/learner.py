#!/usr/bin/env python

import numpy as np
import pandas as pd

from abc import ABCMeta, abstractmethod
from sklearn.cross_validation import KFold


class BaseLearner(object):
    __metaclass__ = ABCMeta

    def __init__(self, n_folds):
        assert isinstance(n_folds, int)

        self.n_folds = n_folds

    def take_scores(self, x, y):
        assert isinstance(x, pd.DataFrame)
        assert isinstance(y, pd.Series)

        kf = KFold(len(y), n_folds=self.n_folds, indices=False)
        scores = []
        for train, test in kf:
            classifier = self.learn(x[train], y[train])
            predictions = classifier.predict(x[test])
            scores.append(self.err(y[test], predictions))
        return np.array(scores)

    @abstractmethod
    def learn(self, x, y):
        pass

    @abstractmethod
    def err(self, y, predictions):
        pass