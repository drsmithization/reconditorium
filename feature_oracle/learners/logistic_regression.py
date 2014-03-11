from learner import BaseLearner
from sklearn.metrics import f1_score
from sklearn import linear_model


class LogisticRegression(BaseLearner):
    def __init__(self, n_folds):
        super(LogisticRegression, self).__init__(n_folds)

    def learn(self, x, y):
        logreg = linear_model.LogisticRegression()
        return logreg.fit(x, y)

    def err(self, y, predictions):
        return f1_score(y, predictions)