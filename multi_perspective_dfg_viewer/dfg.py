import pandas as pd
from multi_perspective_dfg_viewer.dfg_parameters import DFGParameters
from collections import defaultdict
from datetime import timedelta


class DirectlyFollowsGraph:
    def __init__(self, log: pd.DataFrame, parameters: DFGParameters):
        self.log = log
        self.parameters = parameters
        self.start_activities = {}
        self.end_activities = {}
        self.activities = defaultdict(self.activities_factory())
        self.connections = defaultdict(self.connections_factory())

    def activities_factory(self):
        factory_dict = {}
        if self.parameters.calculate_frequency:
            factory_dict["frequency"] = []
        if self.parameters.calculate_time:
            factory_dict["time"] = []
        if self.parameters.calculate_cost:
            factory_dict["cost"] = []
        return lambda: factory_dict

    def connections_factory(self):
        factory_dict = {}
        if self.parameters.calculate_frequency:
            factory_dict["frequency"] = []
        if self.parameters.calculate_time:
            factory_dict["time"] = []
        return lambda: factory_dict

    def build(self):
        grouped_by_case_id = self.log.groupby(
            by=self.parameters.case_id_key, dropna=True, sort=False
        )

        for _, group_data in grouped_by_case_id:
            group_data = group_data.sort_values(by=self.parameters.timestamp_key)

        pass

    def add_activity(self):
        pass

    def add_connection(self):
        pass

    def get_start_activities(self):
        grouped_by_case_id = self.log.groupby(
            self.parameters.case_id_key, dropna=True, sort=False
        )
        start_activities = dict(
            grouped_by_case_id[self.parameters.activity_key].first().value_counts()
        )
        return start_activities

    def get_end_activities(self):
        grouped_by_case_id = self.log.groupby(
            self.parameters.case_id_key, dropna=True, sort=False
        )
        end_activities = dict(
            grouped_by_case_id[self.parameters.activity_key].last().value_counts()
        )
        return end_activities


DFG = DirectlyFollowsGraph
