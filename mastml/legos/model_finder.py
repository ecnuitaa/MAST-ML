"""
Provides a name_to_constructor dict for all the models in sklearn,
and the check_models_mixed function
"""
import warnings

import sklearn.base
import sklearn.utils.testing
import numpy as np

#from . import keras_models
from .. import utils

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    name_to_constructor = dict(sklearn.utils.testing.all_estimators())


class AlwaysFive(sklearn.base.RegressorMixin):
    def __init__(self, constant = 5):
        self.five = constant
    def fit(self, X, y, groups=None):
        return self
    def predict(self, X):
        return np.array([self.five for _ in range(len(X))])

class RandomGuesser(sklearn.base.RegressorMixin):
    def __init__(self):
        pass
    def fit(self, X, y, groups=None):
        self.possible_answers = y
        return self
    def predict(self, X):
        return np.random.choice(self.possible_answers, size=X.shape[0])

custom_models = {
    'AlwaysFive': AlwaysFive,
    'RandomGuesser': RandomGuesser,
    #'DNNClassifier': keras_models.DNNClassifier
}

name_to_constructor.update(custom_models)

def find_model(model_name):
    """ looks up model name using sklearn """
    try:
        return name_to_constructor[model_name]
    except KeyError:
        raise utils.InvalidModel(f"Model '{model_name}' does not exist in scikit-learn.")

def check_models_mixed(model_names):
    """ raises MixedModelsError if models are not all class or all regress """
    found_classifier = found_regressor = False
    for name in model_names:
        if name in custom_models: continue
        class1 = find_model(name)
        if issubclass(class1, sklearn.base.ClassifierMixin):
            found_classifier = True
        elif issubclass(class1, sklearn.base.RegressorMixin):
            found_regressor = True
        else:
            raise Exception(f"Model '{name}' is neither a classifier nor a regressor")

    if found_classifier and found_regressor:
        raise Exception("Both classifiers and regressor models have been included")

    return found_classifier

