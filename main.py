import base64
import os
import pandas as pd

from IPython.display import Image, display

import dfg_visualizer


def pretty_print_dict(dictionary, indent=0):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            print(" " * indent + f"{key}:")
            pretty_print_dict(value, indent + 4)
        else:
            print(" " * indent + f"{key}: {value}")


event_log_path = os.path.join("data", "blasting_with_rework_event_log.csv")

event_log = pd.read_csv(event_log_path, sep=";")

event_log = dfg_visualizer.log_formatter(event_log)

(
    multi_perspective_dfg,
    start_activities,
    end_activities,
) = dfg_visualizer.discover_multi_perspective_dfg(
    event_log,
    calculate_cost=True,
    calculate_frequency=True,
    calculate_time=True,
    frequency_statistic="absolute-activity",
    time_statistic="median",
    cost_statistic="max",
)

dfg_string = dfg_visualizer.get_multi_perspective_dfg_string(
    multi_perspective_dfg,
    start_activities,
    end_activities,
    visualize_frequency=True,
    visualize_time=True,
    visualize_cost=True,
    cost_currency="USD",
    rankdir="TD",
)


def mm(graph):
    graphbytes = graph.encode("ascii")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    Image(url="https://mermaid.ink/img/" + base64_string)


mm(dfg_string)


with open("dfg_string.txt", "w") as f:
    f.write(dfg_string)
