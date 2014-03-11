#!/usr/bin/env python

import pandas as pd
import re


def read_libsvm(fileobject, class_label, default_value=0):
    data = []

    for line in fileobject:
        values = re.split("\s+", line.rstrip())
        class_label_value = values[0]
        data_object = {class_label: int(class_label_value)}
        for value in values[1:]:
            feature, feature_value = value.split(":")
            data_object[feature] = float(feature_value)
        data.append(data_object)

    df = pd.DataFrame(data)

    if not default_value is None:
        df.fillna(default_value, inplace=True)
    return df
