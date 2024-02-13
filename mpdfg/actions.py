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
# from dfg_visualizer.diagrammers.mermaid import MermaidDiagrammer


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
    """
    Discovers a multi-perspective Directly-Follows Graph (DFG) from a log.

    Args:
        log (pd.DataFrame): The event log as a pandas DataFrame.
        case_id_key (str, optional): The column name for the case ID. Defaults to "case:concept:name".
        activity_key (str, optional): The column name for the activity name. Defaults to "concept:name".
        timestamp_key (str, optional): The column name for the timestamp. Defaults to "time:timestamp".
        start_timestamp_key (str, optional): The column name for the start timestamp. Defaults to "start_timestamp".
        cost_key (str, optional): The column name for the cost. Defaults to "cost:total".
        calculate_frequency (bool, optional): Whether to calculate activity frequencies. Defaults to True.
        calculate_time (bool, optional): Whether to calculate activity times. Defaults to True.
        calculate_cost (bool, optional): Whether to calculate activity costs. Defaults to True.
        frequency_statistic (str, optional): The statistic to use for activity frequencies. Defaults to "absolute-activity".
        time_statistic (str, optional): The statistic to use for activity times. Defaults to "mean".
        cost_statistic (str, optional): The statistic to use for activity costs. Defaults to "mean".

    Returns:
        Tuple[dict, dict, dict]: A tuple containing the multi-perspective DFG, start activities, and end activities.
    """
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
    cost_currency: str = "USD",
    rankdir: str = "TD",
):
    """
    Creates a string representation of a multi-perspective Directly-Follows Graph (DFG) diagram.

    Args:
        multi_perspective_dfg (dict): A dictionary representing the multi-perspective DFG.
        start_activities (dict): A dictionary containing the start activities of the DFG.
        end_activities (dict): A dictionary containing the end activities of the DFG.
        visualize_frequency (bool, optional): Whether to visualize the frequency of activities. Defaults to True.
        visualize_time (bool, optional): Whether to visualize the time of activities. Defaults to True.
        visualize_cost (bool, optional): Whether to visualize the cost of activities. Defaults to True.
        cost_currency (str, optional): The currency symbol to use for cost visualization. Defaults to "USD".
        rankdir (str, optional): The direction of the graph layout. Defaults to "TD".

    Returns:
        str: The string representation of the multi-perspective DFG diagram.
    """

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
    cost_currency: str = "USD",
    rankdir: str = "TD",
):
    """
    Visualizes a multi-perspective Directly-Follows Graph (DFG) using graphviz.

    Args:
        multi_perspective_dfg (dict): A dictionary representing the multi-perspective DFG.
        start_activities (dict): A dictionary mapping start activities to their respective frequencies.
        end_activities (dict): A dictionary mapping end activities to their respective frequencies.
        visualize_frequency (bool, optional): Whether to visualize the frequency of activities. Defaults to True.
        visualize_time (bool, optional): Whether to visualize the time of activities. Defaults to True.
        visualize_cost (bool, optional): Whether to visualize the cost of activities. Defaults to True.
        cost_currency (str): The currency symbol to be displayed with the cost. Defaults to "USD".
        rankdir (str, optional): The direction of the graph layout. Defaults to "TD" (top-down).
    """
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
    src = Source(dfg_string, tmp_file.name, format="png")

    render = src.render(cleanup=True)
    shutil.copyfile(render, tmp_file.name)

    img = mpimg.imread(tmp_file.name)
    plt.axis("off")
    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    plt.imshow(img)
    plt.show()


def save_vis_multi_perspective_dfg(
    multi_perspective_dfg: dict,
    start_activities: dict,
    end_activities: dict,
    file_path: str,
    visualize_frequency: bool = True,
    visualize_time: bool = True,
    visualize_cost: bool = True,
    cost_currency: str = "USD",
    format: str = "png",
    rankdir: str = "TD",
):
    """
    Save a visual representation of a multi-perspective Directly-Follows Graph (DFG) to a file.

    Parameters:
        multi_perspective_dfg (dict): The multi-perspective DFG.
        start_activities (dict): A dictionary mapping start activities to their respective labels.
        end_activities (dict): A dictionary mapping end activities to their respective labels.
        file_path (str): The path to save the visual representation file.
        visualize_frequency (bool, optional): Whether to visualize the frequency of activities. Defaults to True.
        visualize_time (bool, optional): Whether to visualize the time of activities. Defaults to True.
        visualize_cost (bool, optional): Whether to visualize the cost of activities. Defaults to True.
        cost_currency (str, optional): The currency used for cost visualization. Defaults to "USD".
        format (str, optional): The format of the visual representation file. Defaults to "png".
        rankdir (str, optional): The direction of the graph layout. Defaults to "TD".
    """
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
