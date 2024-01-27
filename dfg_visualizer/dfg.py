import pandas as pd
from dfg_visualizer.dfg_parameters import DirectlyFollowsGraphParameters
from dfg_visualizer.dfg_builder import DirectlyFollowsGraphBuilder


class DirectlyFollowsGraph:
    def __init__(self, log: pd.DataFrame, parameters: DirectlyFollowsGraphParameters):
        self.log = log
        self.parameters = parameters
        self.start_activities = {}
        self.end_activities = {}
        self.activities = {}
        self.connections = {}

    def build(self):
        DirectlyFollowsGraphBuilder(self, self.log, self.parameters).start()
        breakpoint()

    def visualize(self):
        pass

    def save(self):
        pass

    def get_graph(self):
        return {"activities": self.activities, "connections": self.connections}

    def get_start_activities(self):
        return self.start_activities

    def get_end_activities(self):
        return self.end_activities
