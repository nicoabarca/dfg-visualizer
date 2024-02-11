import os
import pandas as pd
import dfg_visualizer

blasting_event_log_path = os.path.join("data", "blasting_with_rework_event_log.csv")
blasting_event_log = pd.read_csv(blasting_event_log_path, sep=";")

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

blasting_event_log = dfg_visualizer.log_formatter(blasting_event_log, blasting_format)

(
    multi_perspective_dfg,
    start_activities,
    end_activities,
) = dfg_visualizer.discover_multi_perspective_dfg(
    blasting_event_log,
    calculate_cost=True,
    calculate_frequency=True,
    calculate_time=True,
    frequency_statistic="absolute-activity",
    time_statistic="mean",
    cost_statistic="mean",
)


dfg_string = dfg_visualizer.get_multi_perspective_dfg_string(
    multi_perspective_dfg,
    start_activities,
    end_activities,
    visualize_frequency=True,
    visualize_time=True,
    visualize_cost=True,
    cost_currency="USD",
    rankdir="TB",
)

with open("dfg_string.txt", "w") as f:
    f.write(dfg_string)
