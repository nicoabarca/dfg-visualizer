from dfg_visualizer.utils.visualizer import (
    get_dimensions_min_and_max,
    hsl_interpolation_color,
    text_color,
    format_time,
    link_width,
)


class DirectlyFollowsGraphVisualizer:
    def __init__(
        self,
        dfg: dict,
        start_activities: dict,
        end_activities: dict,
        visualize_frequency: bool = True,
        visualize_time: bool = True,
        time_unit: str = "seconds",  # seconds, minutes, hours
        visualize_cost: bool = True,
        cost_currency: str = "USD",  # currency
        rankdir: str = "TD",
    ):
        self.dfg = dfg
        self.start_activities = start_activities
        self.end_activities = end_activities
        self.visualize_frequency = visualize_frequency
        self.visualize_time = visualize_time
        self.time_unit = time_unit
        self.visualize_cost = visualize_cost
        self.cost_currency = cost_currency
        self.rankdir = rankdir
        self.diagram_string = ""
        self.links_counter = 0
        self.link_styles_string = ""
        self.dimensions_min_and_max = get_dimensions_min_and_max(
            self.dfg["activities"], self.dfg["connections"]
        )
        self.build_string()

    def build_string(self):
        self.add_titles()
        self.add_activities()
        self.add_connections()
        self.add_class_definitions()
        self.add_link_styles()
        # TODO: add links styles

    def add_titles(self):
        self.diagram_string += f"flowchart {self.rankdir}\n"
        self.diagram_string += 'start(("&nbsp;fa:fa-play&nbsp;"))\n'
        self.diagram_string += 'complete(("&nbsp;fa:fa-stop&nbsp;"))\n'

    def add_activities(self):
        for activity, dimensions in self.dfg["activities"].items():
            activity_string = ""
            for dimension in dimensions:
                dimension_measure = self.dfg["activities"][activity][dimension]
                color = hsl_interpolation_color(
                    dimension_measure, dimension, self.dimensions_min_and_max[dimension]
                )
                activity_string += self.build_activity_string(
                    activity, dimension, dimension_measure, color
                )

            self.diagram_string += (
                f"{activity.replace(' ', '_')}(\"{activity_string}\")\n"
            )

    def add_connections(self):
        self.add_start_connections()
        for connection, dimensions in self.dfg["connections"].items():
            connections_string = ""
            for dimension in dimensions:
                dimension_measure = self.dfg["connections"][connection][dimension]
                color = hsl_interpolation_color(
                    dimension_measure, dimension, self.dimensions_min_and_max[dimension]
                )
                connections_string += self.build_connection_string(
                    dimension, dimension_measure, color
                )
                if dimension == "frequency":
                    self.link_styles_string += f"linkStyle {self.links_counter} stroke-width: {link_width(dimension_measure, self.dimensions_min_and_max['frequency'])}px;\n"
                    self.links_counter += 1

            self.diagram_string += f"{connection[0].replace(' ', '_')}-->|\"{connections_string}\"|{connection[1].replace(' ', '_')}\n"

        self.add_end_connections()

    def add_start_connections(self):
        start_connections_string = ""
        for activity, frequency in self.start_activities.items():
            color = hsl_interpolation_color(
                frequency, "frequency", self.dimensions_min_and_max["frequency"]
            )
            connection_string = f"start -.\"<span style='background-color: snow; color: {color};'>{frequency}</span>\".- {activity.replace(' ', '_')}\n"
            start_connections_string += connection_string

            self.link_styles_string += f"linkStyle {self.links_counter} stroke-width: {link_width(frequency, self.dimensions_min_and_max['frequency'])}px;\n"
            self.links_counter += 1
        self.diagram_string += start_connections_string

    def add_end_connections(self):
        end_connections_string = ""
        for activity, frequency in self.end_activities.items():
            color = hsl_interpolation_color(
                frequency, "frequency", self.dimensions_min_and_max["frequency"]
            )
            connections_string = f"{activity.replace(' ', '_')} -.\"<span style='background-color: snow; color: {color};'>{frequency}</span>\".- complete\n"
            end_connections_string += connections_string

            self.link_styles_string += f"linkStyle {self.links_counter} stroke-width: {link_width(frequency, self.dimensions_min_and_max['frequency'])}px;\n"
            self.links_counter += 1

        self.diagram_string += end_connections_string

    def add_class_definitions(self):
        formatted_activity_classes = [
            activity.replace(" ", "_") for activity in self.dfg["activities"].keys()
        ]
        activity_classes_string = ",".join(formatted_activity_classes)

        self.diagram_string += f"class {activity_classes_string} activityClass\n"
        self.diagram_string += "class start startClass\n"
        self.diagram_string += "class complete completeClass\n"
        self.diagram_string += (
            "classDef activityClass fill:#FFF,stroke:#FFF,stroke-width:0px\n"
        )
        self.diagram_string += "classDef startClass fill:lime\n"
        self.diagram_string += "classDef completeClass fill:red\n"

    def add_link_styles(self):
        self.diagram_string += self.link_styles_string

    def build_activity_string(self, activity, dimension, dimension_measure, bg_color):
        if dimension == "frequency" and self.visualize_frequency:
            return f"<div style='background-color: {bg_color};  border: 1px solid black; color: {text_color(bg_color)}; '>&nbsp;{activity} ({dimension_measure})&nbsp;</div>"
        if dimension == "time" and self.visualize_time:
            return f"<div style='background-color: {bg_color}; border: 1px solid black; color: {text_color(bg_color)};'>&nbsp;{format_time(dimension_measure)}&nbsp;</div>"
        if dimension == "cost" and self.visualize_cost:
            return f"<div style='background-color: {bg_color}; border: 1px solid black;  color: {text_color(bg_color)};'>&nbsp;{dimension_measure} {self.cost_currency}&nbsp;</div>"
        return ""

    def build_connection_string(self, dimension, dimension_measure, color):
        if dimension == "frequency" and self.visualize_frequency:
            return f"<span style='background-color: snow; color: {color};'>{dimension_measure}</span></br>"
        if dimension == "time" and self.visualize_time:
            return f"<span style='background-color: snow; color: {color};'>{format_time(dimension_measure)}</span></br>"
        return ""

    def get_string(self):
        return self.diagram_string
