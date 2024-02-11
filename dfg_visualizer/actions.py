import pandas as pd
import tempfile
import shutil
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from typing import Tuple
from graphviz import Source
from dfg_visualizer.dfg import DirectlyFollowsGraph
from dfg_visualizer.dfg_parameters import DirectlyFollowsGraphParameters
from dfg_visualizer.diagrammers.graphviz import GraphVizDiagrammer
from dfg_visualizer.diagrammers.mermaid import MermaidDiagrammer


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
    cost_currency: str = "",
    rankdir: str = "TD",
):
    diagrammer = GraphVizDiagrammer(
        multi_perspective_dfg,
        start_activities,
        end_activities,
        visualize_frequency,
        visualize_time,
        visualize_cost,
        cost_currency,
        rankdir,
    )
    diagrammer.build_diagram()
    diagram_string = diagrammer.get_diagram_string()
    return diagram_string


def view_multi_perspective_dfg(
    multi_perspective_dfg: dict,
    start_activities: dict,
    end_activities: dict,
    visualize_frequency: bool = True,
    visualize_time: bool = True,
    visualize_cost: bool = True,
    rankdir: str = "TD",
):
    dfg_string = get_multi_perspective_dfg_string(
        multi_perspective_dfg=multi_perspective_dfg,
        start_activities=start_activities,
        end_activities=end_activities,
        visualize_frequency=visualize_frequency,
        visualize_time=visualize_time,
        visualize_cost=visualize_cost,
        rankdir=rankdir,
    )

    tmp_file = tempfile.NamedTemporaryFile(suffix=".gv")
    tmp_file.close()
    src = Source(dfg_string, tmp_file.name, format="png")

    render = src.render(cleanup=True)
    shutil.copyfile(render, tmp_file.name)

    img = mpimg.imread(tmp_file.name)
    plt.axis("off")
    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    plt.imshow(img)
    plt.show()

    return dfg_string


def save_vis_multi_perspective_dfg(
    multi_perspective_dfg: dict,
    start_activities: dict,
    end_activities: dict,
    file_path: str,
    visualize_frequency: bool = True,
    visualize_time: bool = True,
    visualize_cost: bool = True,
    cost_currency: str = "",
    format: str = "png",
    rankdir: str = "TD",
):
    dfg_string = get_multi_perspective_dfg_string(
        multi_perspective_dfg=multi_perspective_dfg,
        start_activities=start_activities,
        end_activities=end_activities,
        visualize_frequency=visualize_frequency,
        visualize_time=visualize_time,
        visualize_cost=visualize_cost,
        cost_currency=cost_currency,
        rankdir=rankdir,
    )
    tmp_file = tempfile.NamedTemporaryFile(suffix=".gv")
    tmp_file.close()
    src = Source(dfg_string, tmp_file.name, format=format)

    render = src.render(cleanup=True)
    shutil.copyfile(render, f"{file_path}.{format}")
