import numpy as np


def absolute_activity():
    pass


def absolute_case():
    pass


def relative_activity():
    pass


def relative_case():
    pass


def get_dimension_statistic():
    pass


statistical_functions = {
    "absolute-activity": absolute_activity,
    "absolute-case": absolute_case,
    "relative-activity": relative_activity,
    "relative-case": relative_case,
    "mean": np.mean,
    "median": np.median,
    "sum": np.sum,
    "max": np.max,
    "min": np.min,
    "stdev": np.std,
}
