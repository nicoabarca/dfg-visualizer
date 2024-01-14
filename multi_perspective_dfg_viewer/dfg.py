import pandas as pd
from multi_perspective_dfg_viewer.dfg_parameters import DirectlyFollowsGraphParameters
from collections import defaultdict


class DirectlyFollowsGraph:
    def __init__(self, log: pd.DataFrame, parameters: DirectlyFollowsGraphParameters):
        self.log = log
        self.parameters = parameters
        self.start_activities = {}
        self.end_activities = {}
        self.activities = defaultdict(self.activities_factory())
        self.connections = defaultdict(self.connections_factory())

    def activities_factory(self):
        factory_dict = {}
        if self.parameters.calculate_frequency:
            factory_dict["frequency"] = 0
        if self.parameters.calculate_time:
            factory_dict["time"] = []
        if self.parameters.calculate_cost:
            factory_dict["cost"] = []
        return lambda: factory_dict

    def connections_factory(self):
        factory_dict = {}
        if self.parameters.calculate_frequency:
            factory_dict["frequency"] = 0
        if self.parameters.calculate_time:
            factory_dict["time"] = []
        return lambda: factory_dict

    def build(self):
        grouped_by_case_id = self.log.groupby(
            by=self.parameters.case_id_key, dropna=True, sort=False
        )
        for _, group_data in grouped_by_case_id:
            group_data = group_data.sort_values(by=self.parameters.timestamp_key)
            self.update_graph(group_data)

        # TODO: compute graph statistics based on graph data

    def update_graph(self, group_data):
        group_rows_quantity = group_data.shape[0]
        for index in range(group_rows_quantity):
            actual_activity = group_data.iloc[index]
            prev_activity = group_data.iloc[index - 1] if index > 0 else None
            self.update_activities(actual_activity)
            self.update_connections(prev_activity, actual_activity)

    def update_activities(self, activity):
        activity_name = activity[self.parameters.activity_key]
        activity_time = (
            activity[self.parameters.timestamp_key]
            - activity[self.parameters.start_timestamp_key]
        )
        activity_cost = activity[self.parameters.cost_key]
        self.update_activity_data(activity_name, activity_time, activity_cost)

    def update_activity_data(self, name, time, cost):
        if self.parameters.calculate_frequency:
            self.activities[name]["frequency"] += 1
        if self.parameters.calculate_time:
            self.activities[name]["time"].append(time)
        if self.parameters.calculate_cost:
            self.activities[name]["cost"].append(cost)

    def update_connections(self, prev_activity, actual_activity):
        if prev_activity is not None:
            connection_name = (
                prev_activity[self.parameters.activity_key],
                actual_activity[self.parameters.activity_key],
            )
            time_between_activities = (
                actual_activity[self.parameters.start_timestamp_key]
                - prev_activity[self.parameters.timestamp_key]
            )
            self.update_connection_data(connection_name, time_between_activities)

    def update_connection_data(self, name, time_between_activities):
        if self.parameters.calculate_frequency:
            self.connections[name]["frequency"] += 1
        if self.parameters.calculate_time:
            self.connections[name]["time"].append(time_between_activities)

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
