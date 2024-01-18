from dfg_visualizer.dfg import DirectlyFollowsGraph


class DirectlyFollowsGraphVisualizer:
    def __init__(self, dfg: DirectlyFollowsGraph, rankdir: str):
        self.dfg = dfg
        self.rankir = rankdir
        self.diagram_string = ""



    def build_string(self):
        self.add_titles()

    def add_titles(self):
        self.diagram_string += f"flowchart {self.rankdir}\n"
        self.diagram_string += "start((\"&nbsp;fa:fa-play&nbsp;\"))\n"
        self.diagram_string += "complete((\"&nbsp;fa:fa-stop&nbsp;\"))\n"

    def add_activities(self):
        for activity, data in self.dfg.activities:
         
        pass

    def add_links(self):
        pass
