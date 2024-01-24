from dfg_visualizer.dfg import DirectlyFollowsGraph


class DirectlyFollowsGraphVisualizer:
    def __init__(
        self,
        dfg: dict,
        start_activities: dict,
        end_activities: dict,
        visualize_frequency: bool = True,
        visualize_time: bool = True,
        visualize_cost: bool = True,
        rankdir: str = "LR",
    ):
        self.dfg = dfg
        self.start_activities = start_activities
        self.end_activities = end_activities
        self.visualize_frequency = visualize_frequency
        self.visualize_time = visualize_time
        self.visualize_cost = visualize_cost
        self.rankdir = rankdir
        self.diagram_string = ""

    def build_string(self):
        self.add_titles()
        self.add_activities()
        self.add_connections()
        self.add_class_definitions()
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
                activity_string += self.build_activity_string(
                    activity, dimension, dimension_measure
                )

            self.diagram_string += (
                f"{activity.replace(' ', '_')}(\"{activity_string}\")\n"
            )

    def add_start_connection(self):
        self.diagram_string += f"start -.\"<span style='background-color: snow; color: royalblue;'>{list(self.start_activities.values())[0]}</span>\".- {list(self.start_activities.keys())[0].replace(' ', '_')}\n"

    def add_connections(self):
        self.add_start_connection()
        for connection, dimensions in self.dfg["connections"].items():
            connections_string = ""
            for dimension in dimensions:
                dimension_measure = self.dfg["connections"][connection][dimension]
                connections_string += self.build_connection_string(
                    dimension, dimension_measure
                )
            self.diagram_string += f"{connection[0].replace(' ', '_')}-->|\"{connections_string}\"|{connection[1].replace(' ', '_')}\n"
        self.add_end_connection()

    def add_end_connection(self):
        self.diagram_string += f"{list(self.end_activities.keys())[0].replace(' ', '_')} -.\"<span style='background-color: snow; color: royalblue;'>{list(self.end_activities.values())[0]}</span>\".- complete\n"

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

    def build_activity_string(self, activity, dimension, dimension_measure):
        if dimension == "frequency":
            return f"<div style='background-color: royalblue;  border: 1px solid black; '>&nbsp;{activity} ({dimension_measure})&nbsp;</div>"
        elif dimension == "time":
            return f"<div style='background-color: darksalmon; border: 1px solid black'>&nbsp;{dimension_measure}&nbsp;</div>"
        else:
            return f"<div style='background-color: lightgreen; border: 1px solid black; '>&nbsp;{dimension_measure} USD&nbsp;</div>"

    def build_connection_string(self, dimension, dimension_measure):
        if dimension == "frequency":
            return f"<span style='background-color: snow; color: skyblue;'>{dimension_measure}</span></br>"
        else:
            return f"<span style='background-color: snow; color: darksalmon;'>{dimension_measure}</span></br>"

    def get_string(self):
        return self.diagram_string
