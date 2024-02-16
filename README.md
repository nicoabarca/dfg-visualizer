# Multi Perspective DFG Visualizer

 A package to visualize multi perspective Directly-Follows Graphs (DFG) based on event logs. It aims to provide insights into the relationships and dependencies between different perspectives in a given process.


# Installation
This package runs under Python 3.9+, use [pip](https://pip.pypa.io/en/stable/) to install.
```sh
pip install mpdfg
```
To render and save a generated diagram, you also need to install [Graphviz](https://www.graphviz.org)

# Quickstart

### Format event log
Using `mpdfg.log_formatter` you can format your own initial event log with the corresponding column names, based on [pm4py](https://pm4py.fit.fraunhofer.de) standard way of naming logs columns.

The format dictionary to pass as argument to this function needs to have the following structure:
```py
{
    "case:concept:name": <Case Id>, # required
    "concept:name": <Activity Id>, # required
    "time:timestamp": <Timestamp>, # required
    "start_timestamp": <Start Timestamp>, # optional
    "org:resource": <Resource>, # optional
    "cost:total": <Cost>, # optional
}
```

Each value of the dictionary needs to match the corresponding column name of the initial event log. If `start_timestamp`, `org:resource` and `cost:total` are not present in your event log, you can leave its values as blank strings.

```py
import mpdfg
import pandas as pd

raw_event_log = pd.read_csv("raw_event_log.csv")

format_dictionary = {
    "case:concept:name": "Case ID",
    "concept:name": "Activity",
    "time:timestamp": "Complete",
    "start_timestamp": "Start",
    "org:resource": "Resource",
    "cost:total": "Cost",
}

event_log = mpdfg.log_formatter(raw_event_log, format_dictionary)

```
### Discover Multi Perspective DFG

```py
(
    multi_perspective_dfg,
    start_activities,
    end_activities,
) = mpdfg.discover_multi_perspective_dfg(
    event_log,
    calculate_cost=True,
    calculate_frequency=True,
    calculate_time=True,
    frequency_statistic="absolute-activity",
    time_statistic="mean",
    cost_statistic="mean",
)

```

### Get the DFG diagram string representation
```py
mpdfg_string = mpdfg.get_multi_perspective_dfg_string(
    multi_perspective_dfg,
    start_activities,
    end_activities,
    visualize_frequency=True,
    visualize_time=True,
    visualize_cost=True,
    rankdir="TB",
    diagram_tool="graphviz",
)

```

### View the generated DFG diagram
Allows the user to view the diagram in interactive Python environments like Jupyter Notebooks and Google Colabs.

```py
mpdfg.view_multi_perspective_dfg(
    multi_perspective_dfg,
    start_activities,
    end_activities,
    file_path="diagram",
    visualize_frequency=True,
    visualize_time=True,
    visualize_cost=True,
    format="png",
    rankdir="TB",
    diagram_tool="grahpviz",
)
```
### Save the generated DFG diagram

```py
mpdfg.save_vis_multi_perspective_dfg(
    multi_perspective_dfg,
    start_activities,
    end_activities,
    file_path="diagram",
    visualize_frequency=True,
    visualize_time=True,
    visualize_cost=True,
    format="png",
    rankdir="TB",
    diagram_tool="graphviz",
)
```
