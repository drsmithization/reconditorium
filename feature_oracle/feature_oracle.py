#!/usr/bin/env python

import argparse
import sys
import traceback

import numpy as np
import pandas as pd
import scipy as sp
import scikits.bootstrap as bootstrap

from learners.logistic_regression import LogisticRegression


class InputDataError(Exception):
    pass


def shuffle_data(df):
    return df.reindex(np.random.permutation(df.index))


def take_differences(x, y, learner, exclude):
    columns = [c for c in x.columns if c not in exclude]
    a = learner.take_scores(x, y)
    b = learner.take_scores(x[columns], y)
    return a - b, a


def main():
    argparser = argparse.ArgumentParser(description="Evaluate feature profit.")
    argparser.add_argument("-p", "--pool",
                           dest="pool")
    argparser.add_argument("-i", "--id",
                           dest="id")
    argparser.add_argument("-a", "--assessment",
                           dest="assessment")
    argparser.add_argument("-f", "--fold-count",
                           dest="fold_count",
                           type=int)
    argparser.add_argument("-t", "--test",
                           dest="test",
                           action="append")
    args = argparser.parse_args()

    try:
        try:
            data = pd.read_csv(args.pool)
            data = shuffle_data(data)
        except Exception as err:
            raise InputDataError("cannot read data ({0})".format(err))

        if args.assessment not in data:
            raise InputDataError("columns {0} is not in the data".format(args.assessment))
        for t in args.test:
            if t not in data:
                raise InputDataError("columns {0} is not in the data".format(t))

        y = data[args.assessment]
        feature_columns = [c for c in data.columns if c not in [args.id, args.assessment]]
        x = data[feature_columns]

        learner = LogisticRegression(args.fold_count)
        differences, base_scores\
            = take_differences(x, y, learner, args.test)

        _, p_value = sp.stats.wilcoxon(differences)

        print "mean base score: {0:.4f}".format(base_scores.mean())
        print "mean diff: {0:.4f}".format(differences.mean())
        print "WX-test p-value: {0}".format(p_value)

        CIs = bootstrap.ci(data=differences, statfunction=sp.mean)
        print "Bootstrapped 95% confidence intervals (mean diff)\n  Low:", CIs[0], "\n  High:", CIs[1]

        print "\nscores by fold:"
        print "fold base       diff"
        fold_number = 0
        for d, b in zip(differences, base_scores):
            print "{0:<4} {1:<10.4f} {2:<10.4f}".format(fold_number, b, d)
            fold_number += 1

    except InputDataError as err:
        print >>sys.stderr, "Bad input: {0}".format(err)
    except Exception as err:
        print >>sys.stderr, "Error: {0}".format(err)
        traceback.print_exc()


if __name__ == "__main__":
    main()