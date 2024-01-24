import os
import pandas as pd

import dfg_visualizer


def pretty_print_dict(dictionary, indent=0):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            print(" " * indent + f"{key}:")
            pretty_print_dict(value, indent + 4)
        else:
            print(" " * indent + f"{key}: {value}")


event_log_path = os.path.join("data", "blasting_with_rework_event_log_10k.csv")

event_log = pd.read_csv(event_log_path, sep=";")

event_log = dfg_visualizer.log_formatter(event_log)

(
    multi_perspective_dfg,
    start_activities,
    end_activities,
) = dfg_visualizer.discover_multi_perspective_dfg(event_log)

# TESTING
dfg_string = dfg_visualizer.get_multi_perspective_dfg_string(
    multi_perspective_dfg, start_activities, end_activities, rankdir="TD"
)

with open("dfg_string.txt", "w") as f:
    f.write(dfg_string)
print(dfg_string)
