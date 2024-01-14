import pandas as pd
from typing import Tuple
from multi_perspective_dfg_viewer.get_multi_perspective_dfg import (
    get_multi_perspective_dfg,
)
from multi_perspective_dfg_viewer.activities import (
    get_start_activities,
    get_end_activities,
)

from multi_perspective_dfg_viewer.dfg_parameters import DFGParameters
from multi_perspective_dfg_viewer.dfg import DFG


def discover_multi_perspective_dfg(
    log: pd.DataFrame,
    case_id_key: str = "case:concept:name",
    activity_key: str = "concept:name",
    timestamp_key: str = "time:timestamp",
    start_timestamp_key: str = "start_timestamp",
    cost_key: str = "cost:total",
    calculate_frequency: bool = True,
    calculate_time: bool = True,
    calculate_cost: bool = True,
    frequency_statistic: str = "absolute-activity",  # absolute-case, relative-activity, relative-case
    time_statistic: str = "mean",  # mean, median, sum, max, min, stdev
    cost_statistic: str = "mean",  # mean, median, sum, max, min, stdev
) -> Tuple[dict, dict, dict]:
    dfg_parameters = DFGParameters(
        case_id_key,
        activity_key,
        timestamp_key,
        start_timestamp_key,
        cost_key,
        calculate_frequency,
        calculate_time,
        calculate_cost,
        frequency_statistic,
        time_statistic,
        cost_statistic,
    )
    dfg = DFG(log, dfg_parameters)

    # start_activities = get_start_activities(log)
    # end_activities = get_end_activities(log)
    start_activities = {}
    end_activities = {}

    multi_perspective_dfg = get_multi_perspective_dfg(log)

    return multi_perspective_dfg, start_activities, end_activities
