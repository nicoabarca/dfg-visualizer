import pandas as pd
from typing import Tuple
from multi_persperctive_dfg_viewer.get_log_properties import get_log_properties
from multi_persperctive_dfg_viewer.algo.get_multi_perspercitive_dfg import (
    get_multi_perspective_dfg,
)


def discover_multi_perspective_dfg(
    log: pd.DataFrame,
    case_id_key: str = "case:concept:name",
    activity_key: str = "concept:name",
    timestamp_key: str = "time:timestamp",
    start_timestamp_key: str = "start_timestamp",
    cost_key: str = "cost:total",
    calculate_frequency: bool = True,
    calculate_time_performance: bool = True,
    calculate_cost_performance: bool = True,
    frequency_measure: str = "absolute-activity",  # absolute-case, relative-activity, relative-case
    time_measure: str = "mean",  # mean, median, sum, max, min, stdev
    cost_measure: str = "mean",  # mean, median, sum, max, min, stdev
) -> Tuple[dict, dict, dict]:
    start_activities = {}
    end_activities = {}
    multi_perspective_dfg = get_multi_perspective_dfg(log)

    return multi_perspective_dfg, start_activities, end_activities
