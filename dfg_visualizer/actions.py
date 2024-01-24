import pandas as pd
from typing import Tuple
from dfg_visualizer.dfg import DirectlyFollowsGraph
from dfg_visualizer.dfg_parameters import DirectlyFollowsGraphParameters
from dfg_visualizer.dfg_visualizer import DirectlyFollowsGraphVisualizer


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
    frequency_statistic: str = "absolute-activity",
    time_statistic: str = "mean",
    cost_statistic: str = "mean",
) -> Tuple[dict, dict, dict]:
    dfg_parameters = DirectlyFollowsGraphParameters(
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
    dfg = DirectlyFollowsGraph(log, dfg_parameters)
    dfg.build()

    multi_perspective_dfg = dfg.get_graph()
    start_activities = dfg.get_start_activities()
    end_activities = dfg.get_end_activities()

    return multi_perspective_dfg, start_activities, end_activities


def get_multi_perspective_dfg_string(
    multi_perspective_dfg: dict,
    start_activities: dict,
    end_activities: dict,
    visualize_frequency: bool = True,
    visualize_time: bool = True,
    visualize_cost: bool = True,
    rankdir: str = "LR",
):
    dfg_visualizer = DirectlyFollowsGraphVisualizer(
        multi_perspective_dfg,
        start_activities,
        end_activities,
        visualize_frequency,
        visualize_time,
        visualize_cost,
        rankdir,
    )
    dfg_visualizer.build_string()
    dfg_string = dfg_visualizer.get_string()
    return dfg_string


def view_multi_perspective_dfg(
    multi_perspective_dfg: dict,
    start_activities: dict,
    end_activities: dict,
    visualize_frequency: bool = True,
    visualize_time: bool = True,
    visualize_cost: bool = True,
    format: str = "png",  # png, svg, html (según viabilidad; si solo se puede PNG, es OK)
    rankdir: str = "LR",
):
    string = get_multi_perspective_dfg_string(
        multi_perspective_dfg, start_activities, end_activities, rankdir
    )

    return string


def save_vis_multi_perspective_dfg(
    multi_perspective_dfg: dict,
    start_activities: dict,
    end_activities: dict,
    file_path: str,
    visualize_frequency: bool = True,
    visualize_time: bool = True,
    visualize_cost: bool = True,
    format: str = "png",  # png, svg, html (según viabilidad; si solo se puede PNG, es OK)
    rankdir: str = "LR",
):
    string = get_multi_perspective_dfg_string(
        multi_perspective_dfg, start_activities, end_activities, rankdir
    )

    # Guardar diagrama

    return None
