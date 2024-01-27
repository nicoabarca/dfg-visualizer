import numpy as np


def new_activity_dict(dfg_params):
    return {
        key: [] if key != "frequency" else 0
        for key, value in {
            "frequency": dfg_params.calculate_frequency,
            "time": dfg_params.calculate_time,
            "cost": dfg_params.calculate_cost,
        }.items()
        if value
    }


def new_connection_dict(dfg_params):
    return {
        key: [] if key != "frequency" else 0
        for key, value in {
            "frequency": dfg_params.calculate_frequency,
            "time": dfg_params.calculate_time,
        }.items()
        if value
    }


def absolute_activity(activity_frequency, total_cases):
    return activity_frequency


def absolute_case(activity_frequency, total_cases):
    return min(activity_frequency, total_cases)


def relative_activity(activity_frequency, total_cases):  # TODO
    pass


def relative_case(activity_frequency, total_cases):
    relative_percentage = min(1, activity_frequency / total_cases)
    return f"{relative_percentage:.2%}"


def statistics_names_mapping(dfg_params):
    return {
        key: getattr(dfg_params, f"{key}_statistic")
        for key in ["frequency", "cost", "time"]
        if getattr(dfg_params, f"calculate_{key}")
    }


statistics_functions = {
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
