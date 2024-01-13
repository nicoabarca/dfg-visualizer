from dataclasses import dataclass


@dataclass
class DirectlyFollowsGraphParameters:
    case_id_key: str = "case:concept:name"
    activity_key: str = "concept:name"
    timestamp_key: str = "time:timestamp"
    start_timestamp_key: str = "start_timestamp"
    cost_key: str = "cost:total"
    calculate_frequency: bool = True
    calculate_time_performance: bool = True
    calculate_cost_performance: bool = True
    frequency_measure: str = (
        "absolute-activity"  # absolute-case, relative-activity, relative-case
    )
    time_measure: str = "mean"  # mean, median, sum, max, min, stdev
    cost_measure: str = "mean"  # mean, median, sum, max, min, stdev

    def __post_init__(self):
        if self.frequency_measure not in {
            "absolute-activity",
            "absolute-case",
            "relative_activity",
            "relative-case",
        }:
            raise ValueError(
                "Valid values for frequency measure are             absolute-activity, absolute-case,relative_activity,relative-case"
            )

        if self.time_measure not in {"mean", "median", "sum", "max", "min", "stdev"}:
            raise ValueError(
                "Valud values for time measure are mean, median, sum, max, min ,stdev"
            )

        if self.cost_measure not in {"mean", "median", "sum", "max", "min", "stdev"}:
            raise ValueError(
                "Valud values for cost measure are mean, median, sum, max, min ,stdev"
            )


DFGParameters = DirectlyFollowsGraphParameters
