import numpy as np
from sklearn import cross_validation


def train_test_predictions(X, y, train_indices, test_indices, model):
    '''
    Train a model on the given train/test split, and return predictions on the
    test data (and probabilities of the top prediction).

    X is all of your data (a potentially sparse 2D array)
    y is your labels (a numpy array)
    train_indices is either a list of indices or a boolean mask
    test_indices is either a list of indices or a boolean mask
    model is a parameterized scikit-learn model, e.g.,
        model = linear_model.LogisticRegression(penalty='l2')

    Return a tuple of (test_y, pred_y, pred_y_proba), so that you can easily
    get the accuracy by calling (test_y == pred_y).mean()
    '''
    # divide data
    train_X = X[train_indices, :]
    train_y = y[train_indices]
    test_X = X[test_indices, :]
    test_y = y[test_indices]
    # fit model
    model.fit(train_X, train_y)
    # predict on test data
    pred_proba = model.predict_proba(test_X)
    pred_proba_argmax = pred_proba.argmax(axis=1)
    # this has the same effect as: pred_y = model.predict(test_X)
    pred_y = model.classes_[pred_proba_argmax]
    # we must use np.arange(pred_proba.shape[0]), not :, to select all the rows
    pred_y_proba = pred_proba[np.arange(pred_proba.shape[0]), pred_proba_argmax]
    # return tuple of predictions
    return test_y, pred_y, pred_y_proba


def train_test_predictions_iter(X, y, train_size, n_iter, Model):
    '''
    Run train_test_predictions() n_iter times.

    In contrast to train_test_predictions, Model should be a function that
    returns a model, e.g.,
        Model = lambda: linear_model.LogisticRegression(penalty='l2')

    Example:
        df = pd.DataFrame(train_test_predictions_iter(X, y, 0.9, 10, Model))

    Uses cross_validation.ShuffleSplit to pick random indices.
    '''
    # when test_size is None, the complement of train_size will be used.
    folds = cross_validation.ShuffleSplit(len(y), n_iter=n_iter, train_size=train_size, test_size=None)
    for i, (train_indices, test_indices) in enumerate(folds):
        fold_info = dict(train_size=len(train_indices), test_size=len(test_indices), iteration=i)
        model = Model()
        test_y, pred_y, pred_y_proba = train_test_predictions(X, y, train_indices, test_indices, model)
        for test_label, pred_label, pred_label_proba in zip(test_y, pred_y, pred_y_proba):
            yield dict(test_label=test_label, pred_label=pred_label, pred_label_proba=pred_label_proba, **fold_info)


def train_test_report(X, y, train_indices, test_indices, model):
    '''
    Run train_test_predictions on the specified train/test split with the given
    model. Return a dict with the overall accuracy and mean and std. dev. on
    the probabilities assigned to the correct predictions and also for the
    incorrect predictions.
    '''
    test_y, pred_y, pred_y_proba = train_test_predictions(X, y, train_indices, test_indices, model)
    # correct_indices is a boolean mask
    correct_indices = test_y == pred_y
    accuracy = (correct_indices).mean()
    error_proba = pred_y_proba[~correct_indices]
    correct_proba = pred_y_proba[correct_indices]
    # create report
    return dict(accuracy=accuracy,
                error_proba_mean=error_proba.mean(), error_proba_std=error_proba.std(),
                correct_proba_mean=correct_proba.mean(), correct_proba_std=correct_proba.std())


def train_test_report_iter(X, y, train_sizes, n_iter, Model):
    '''
    Run train_test_report for n_iter of each of the sizes in train_sizes.
    The yielded dict reports will include all the values of train_test_report's
    returned report, along with the train and test size.

    In contrast to train_test_predictions and train_test_report, Model should be
    a function that returns a model, e.g.,
        Model = lambda: linear_model.LogisticRegression(penalty='l2')

    Example:
        df = pd.DataFrame(train_test_report_iter(X, y, [10, 100, 1000], 10, Model))

    Uses cross_validation.ShuffleSplit to pick random indices.
    '''
    for train_size in train_sizes:
        # when test_size is None, the complement of train_size will be used.
        folds = cross_validation.ShuffleSplit(len(y), n_iter=n_iter, train_size=train_size, test_size=None)
        for _, (train_indices, test_indices) in enumerate(folds):
            model = Model()
            report = train_test_report(X, y, train_indices, test_indices, model)
            yield dict(train=len(train_indices), test=len(test_indices), **report)
