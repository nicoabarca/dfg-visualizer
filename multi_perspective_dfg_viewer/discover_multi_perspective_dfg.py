import pandas as pd
from typing import Tuple
from multi_perspective_dfg_viewer.get_multi_perspective_dfg import (
    get_multi_perspective_dfg,
)
from multi_perspective_dfg_viewer.activities import (
    get_start_activities,
    get_end_activities,
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
    start_activities = get_start_activities(log)
    end_activities = get_end_activities(log)
    multi_perspective_dfg = get_multi_perspective_dfg(log)

    return multi_perspective_dfg, start_activities, end_activities
