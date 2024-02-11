import os
import pandas as pd
import dfg_visualizer

blasting_event_log_path = os.path.join("data", "blasting_with_rework_event_log.csv")
road_traffic_event_log_path = os.path.join("data", "Road_Traffic_Fine_Management_Process.csv")

blasting_event_log = pd.read_csv(blasting_event_log_path, sep=";")
road_traffic_event_log = pd.read_csv(road_traffic_event_log_path, sep=",")

# Key is the column format name of pm4py
# Value is the column name of the specific log and soon to be changed
# We will always need 3 columns for case, activity and timestamp
blasting_format = {
    "case:concept:name": "Case ID",
    "concept:name": "Activity",
    "time:timestamp": "Complete",
    "start_timestamp": "Start",
    "org:resource": "Resource",
    "cost:total": "Cost",
}

road_traffic_format = {
    "case:concept:name": "Case ID",
    "concept:name": "Activity",
    "time:timestamp": "Complete Timestamp",
    "start_timestamp": "",
    "org:resource": "Resource",
    "cost:total": "",
}

blasting_event_log = dfg_visualizer.log_formatter(blasting_event_log, blasting_format)
road_traffic_event_log = dfg_visualizer.log_formatter(road_traffic_event_log, road_traffic_format)

# (
#     multi_perspective_dfg,
#     start_activities,
#     end_activities,
# ) = dfg_visualizer.discover_multi_perspective_dfg(
#     road_traffic_log,
#     calculate_cost=True,
#     calculate_frequency=True,
#     calculate_time=True,
#     frequency_statistic="absolute-activity",
#     time_statistic="mean",
#     cost_statistic="mean",
# )

freq_statistics = ["absolute-activity", "absolute-case", "relative-case", "relative-activity"]
numbers_statistics = ["mean", "min", "max", "stdev", "median", "sum"]


for fs in freq_statistics:
    for ns in numbers_statistics:
        print(fs, ns)
        (
            multi_perspective_dfg,
            start_activities,
            end_activities,
        ) = dfg_visualizer.discover_multi_perspective_dfg(
            blasting_event_log,
            calculate_cost=True,
            calculate_frequency=True,
            calculate_time=True,
            frequency_statistic=fs,
            time_statistic=ns,
            cost_statistic=ns,
        )
        dfg_visualizer.save_vis_multi_perspective_dfg(
            multi_perspective_dfg,
            start_activities,
            end_activities,
            file_path=f"imgs/fs_{fs}_ns_{ns}",
            visualize_frequency=True,
            visualize_time=True,
            visualize_cost=True,
            format="png",
            rankdir="TB",
        )
