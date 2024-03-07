import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tempfile
import shutil
from graphviz import Source
from typing import Tuple
from mpdfg.utils.actions import save_graphviz_diagram, save_mermaid_diagram, image_size
from mpdfg.dfg import DirectlyFollowsGraph
from mpdfg.dfg_parameters import DirectlyFollowsGraphParameters
from mpdfg.diagrammers.graphviz import GraphVizDiagrammer
from mpdfg.diagrammers.mermaid import MermaidDiagrammer


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
        frequency_statistic (str , optional): The statistic to use for activity frequencies. Valid values are "absolute-activity", "absolute-case", "relative-case" and "relative-activity". Defaults to "absolute-activity".
        time_statistic (str, optional): The statistic to use for activity times. Valid values are "mean", "sum", "max", "min", "median" and "stdev". Defaults to "mean".
        cost_statistic (str, optional): The statistic to use for activity costs. Valid values are "mean, "sum", "max", "min", "median" and "stdev". Defaults to "mean".

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
    diagram_tool: str = "graphviz",
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
        diagram_tool (str, optional): The diagram_tool to use for building the diagram. Valid values are "graphviz" and "mermaid". Defaults to "graphviz".

    Returns:
        str: The string representation of the multi-perspective DFG diagram.

    Note:
        Mermaid diagrammer only supports saving the DFG diagram as a HTML file. It does not support viewing the diagram in interactive Python environments like Jupyter Notebooks and Google Colabs. Also the user needs internet connection to properly show the diagram in the HTML.
    """
    diagrammer = None
    if diagram_tool == "graphviz":
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
    else:
        diagrammer = MermaidDiagrammer(
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
    figsize: Tuple = None,
):
    """
    Visualizes a multi-perspective Directly-Follows Graph (DFG) using graphviz in interactive Python environments.

    Args:
        multi_perspective_dfg (dict): A dictionary representing the multi-perspective DFG.
        start_activities (dict): A dictionary mapping start activities to their respective frequencies.
        end_activities (dict): A dictionary mapping end activities to their respective frequencies.
        visualize_frequency (bool, optional): Whether to visualize the frequency of activities. Defaults to True.
        visualize_time (bool, optional): Whether to visualize the time of activities. Defaults to True.
        visualize_cost (bool, optional): Whether to visualize the cost of activities. Defaults to True.
        cost_currency (str, optional): The currency symbol to be displayed with the cost. Defaults to "USD".
        rankdir (str, optional): The direction of the graph layout. Defaults to "TD" (top-down).
        figsize (Tuple, optional): The width and height of the displayed diagram. Defaults to None.

    Note:
        View of multi perspective DFGs are only supported for diagram strings made with graphviz.
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

    if not figsize:
        figsize = image_size(multi_perspective_dfg, rankdir)

    img = mpimg.imread(tmp_file.name)
    plt.figure(figsize=figsize)
    plt.axis("off")
    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    plt.imshow(img)
    plt.show()


def save_vis_multi_perspective_dfg(
    multi_perspective_dfg: dict,
    start_activities: dict,
    end_activities: dict,
    file_name: str,
    visualize_frequency: bool = True,
    visualize_time: bool = True,
    visualize_cost: bool = True,
    cost_currency: str = "USD",
    format: str = "png",
    rankdir: str = "TD",
    diagram_tool: str = "graphviz",
):
    """
    Save a visual representation of a multi-perspective Directly-Follows Graph (DFG) to a file.

    Parameters:
        multi_perspective_dfg (dict): The multi-perspective DFG.
        start_activities (dict): A dictionary mapping start activities to their respective labels.
        end_activities (dict): A dictionary mapping end activities to their respective labels.
        file_name (str): The path to save the visual representation file.
        visualize_frequency (bool, optional): Whether to visualize the frequency of activities. Defaults to True.
        visualize_time (bool, optional): Whether to visualize the time of activities. Defaults to True.
        visualize_cost (bool, optional): Whether to visualize the cost of activities. Defaults to True.
        cost_currency (str, optional): The currency used for cost visualization. Defaults to "USD".
        format (str, optional): The format of the visual representation file. Defaults to "png". More output formats can be found at https://graphviz.org/docs/outputs
        rankdir (str, optional): The direction of the graph layout. Defaults to "TD".
        diagram_tool (str | "graphviz" | "mermaid", optional): The diagram tool to use for building the diagram. Defaults to "graphviz".

    Note:
        Mermaid diagrammer only supports saving the DFG diagram as a HTML file. It does not support viewing the diagram in interactive Python environments like Jupyter Notebooks and Google Colabs. Also the user needs internet connection to properly show the diagram in the HTML.
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
        diagram_tool=diagram_tool,
    )
    if diagram_tool == "graphviz":
        save_graphviz_diagram(dfg_string, file_name, format)
    elif diagram_tool == "mermaid":
        save_mermaid_diagram(dfg_string, file_name)
    else:
        print("Invalid diagram tool. Options are graphviz and mermaid.")
