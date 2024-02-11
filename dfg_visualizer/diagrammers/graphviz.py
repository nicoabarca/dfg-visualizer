from dfg_visualizer.utils.constants import (
    GRAPH_VIZ_RANKDIR,
    GRAPH_VIZ_START_NODE,
    GRAPH_VIZ_END_NODE,
    GRAPH_VIZ_NODE,
    GRAPH_VIZ_NODE_DATA,
    GRAPH_VIZ_NODE_DATA_ROW,
    GRAPH_VIZ_LINK,
    GRAPH_VIZ_LINK_DATA,
    GRAPH_VIZ_LINK_DATA_ROW,
    GRAPH_VIZ_START_END_LINK,
)

from dfg_visualizer.utils.diagrammer import (
    ids_mapping,
    dimensions_min_and_max,
    hsv_color,
    format_time,
    link_width,
)


class GraphVizDiagrammer:
    def __init__(
        self,
        dfg: dict,
        start_activities: dict,
        end_activities: dict,
        visualize_frequency: bool = True,
        visualize_time: bool = True,
        visualize_cost: bool = True,
        cost_currency: str = "",
        rankdir: str = "TB",
    ):
        self.dfg = dfg
        self.start_activities = start_activities
        self.end_activities = end_activities
        self.visualize_frequency = visualize_frequency
        self.visualize_time = visualize_time
        self.visualize_cost = visualize_cost
        self.cost_currency = cost_currency
        self.rankdir = rankdir
        self.activities_ids = {}
        self.dimensions_min_and_max = {}
        self.diagram_string = ""

        self.set_activities_ids_mapping()
        self.set_dimensions_min_and_max()

    def set_activities_ids_mapping(self):
        self.activities_ids = ids_mapping(self.dfg["activities"])

    def set_dimensions_min_and_max(self):
        self.dimensions_min_and_max = dimensions_min_and_max(
            self.dfg["activities"], self.dfg["connections"]
        )

    def build_diagram(self):
        self.add_config()
        self.add_activities_string()
        self.add_connections_string()
        self.add_graph_type()

    def add_config(self):
        self.diagram_string += GRAPH_VIZ_RANKDIR.format(self.rankdir)
        self.diagram_string += GRAPH_VIZ_START_NODE
        self.diagram_string += GRAPH_VIZ_END_NODE

    def add_activities_string(self):
        for activity in self.dfg["activities"].keys():
            activity_string = self.build_activity_string(activity)
            self.diagram_string += activity_string

    def build_activity_string(self, activity):
        dimensions_string = ""
        for dimension, measure in self.dfg["activities"][activity].items():
            bgcolor, content = self.activity_string_based_on_data(activity, dimension, measure)
            if content != "":
                dimensions_string += GRAPH_VIZ_NODE_DATA_ROW.format(bgcolor, content)

        node_data_string = GRAPH_VIZ_NODE_DATA.format(dimensions_string)
        return GRAPH_VIZ_NODE.format(self.activities_ids[activity], node_data_string)

    def activity_string_based_on_data(self, activity, dimension, measure):
        bgcolor = hsv_color(measure, dimension, self.dimensions_min_and_max[dimension])
        content = ""
        if dimension == "frequency":
            bgcolor = bgcolor if self.visualize_frequency else "royalblue"
            content = (
                f"{activity} ({'{0:,}'.format(measure)})" if self.visualize_frequency else activity
            )

        elif dimension == "time" and self.visualize_time:
            content = format_time(measure)

        elif dimension == "cost" and self.visualize_cost:
            content = f"{'{0:,}'.format(measure)} {self.cost_currency}"

        return bgcolor, content

    def add_connections_string(self):
        self.add_start_and_end_connections_string()
        for connection in self.dfg["connections"].keys():
            connection_string = self.build_connection_string(connection)
            self.diagram_string += connection_string

    def add_start_and_end_connections_string(self):
        for activity, frequency in self.start_activities.items():
            connection_string = GRAPH_VIZ_START_END_LINK.format(
                "start",
                self.activities_ids[activity],
                link_width(frequency, self.dimensions_min_and_max["frequency"])
                if self.visualize_frequency
                else 1,
                "{0:,}".format(frequency) if self.visualize_frequency else "",
            )
            self.diagram_string += connection_string

        for activity, frequency in self.end_activities.items():
            connection_string = GRAPH_VIZ_START_END_LINK.format(
                self.activities_ids[activity],
                "complete",
                link_width(frequency, self.dimensions_min_and_max["frequency"])
                if self.visualize_frequency
                else 1,
                "{0:,}".format(frequency) if self.visualize_frequency else "",
            )
            self.diagram_string += connection_string

    def build_connection_string(self, connection):
        dimensions_string = ""
        for dimension, measure in self.dfg["connections"][connection].items():
            bgcolor, content = self.connection_string_based_on_data(dimension, measure)
            if content != "":
                dimensions_string += GRAPH_VIZ_LINK_DATA_ROW.format(bgcolor, content)

        penwidth = (
            link_width(
                self.dfg["connections"][connection]["frequency"],
                self.dimensions_min_and_max["frequency"],
            )
            if self.visualize_frequency
            else 1
        )

        link_data_string = GRAPH_VIZ_LINK_DATA.format(dimensions_string)

        return GRAPH_VIZ_LINK.format(
            self.activities_ids[connection[0]],
            self.activities_ids[connection[1]],
            penwidth,
            link_data_string,
        )

    def connection_string_based_on_data(self, dimension, measure):
        bgcolor = hsv_color(measure, dimension, self.dimensions_min_and_max[dimension])
        content = ""
        if dimension == "frequency":
            content = "{0:,}".format(measure) if self.visualize_frequency else content
        elif dimension == "time" and self.visualize_time:
            content = format_time(measure)

        return bgcolor, content

    def add_graph_type(self):
        self.diagram_string = "digraph {\n" + self.diagram_string + "}"

    def get_diagram_string(self):
        return self.diagram_string
