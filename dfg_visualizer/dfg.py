import numpy as np
import pandas as pd
from dfg_visualizer.dfg_parameters import DirectlyFollowsGraphParameters


class DirectlyFollowsGraph:
    def __init__(self, log: pd.DataFrame, parameters: DirectlyFollowsGraphParameters):
        self.log = log
        self.parameters = parameters
        self.start_activities = self.get_start_activities()
        self.end_activities = self.get_end_activities()
        self.activities = {}
        self.connections = {}

    def visualize(self):
        pass

    def build(self):
        grouped_by_case_id = self.log.groupby(
            by=self.parameters.case_id_key, dropna=True, sort=False
        )
        for _, group_data in grouped_by_case_id:
            self.update_graph(group_data)

        self.compute_dimensions_statistics()

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
        if name not in self.activities.keys():
            self.activities[name] = self.new_activity_dict()
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
        if name not in self.connections.keys():
            self.connections[name] = self.new_connection_dict()
        if self.parameters.calculate_frequency:
            self.connections[name]["frequency"] += 1
        if self.parameters.calculate_time:
            self.connections[name]["time"].append(time_between_activities)

    def compute_dimensions_statistics(self):
        for activity_name, dimensions in self.activities.items():
            for dimension in dimensions.keys():
                if dimension != "frequency":
                    activity_dimension_data = self.activities[activity_name][dimension]
                    dimension_statistic = self.get_dimension_statistic(dimension)
                    self.activities[activity_name][dimension] = self.compute_statistic(
                        activity_dimension_data, dimension_statistic
                    )
        for connection_name, dimensions in self.connections.items():
            for dimension in dimensions.keys():
                if dimension != "frequency":
                    connection_dimension_data = self.connections[connection_name][
                        dimension
                    ]
                    dimension_statistic = self.get_dimension_statistic(dimension)
                    self.connections[connection_name][
                        dimension
                    ] = self.compute_statistic(
                        connection_dimension_data, dimension_statistic
                    )

    def get_dimension_statistic(self, dimension):
        if dimension == "frequency":
            return self.parameters.frequency_statistic
        if dimension == "time":
            return self.parameters.time_statistic
        if dimension == "cost":
            return self.parameters.cost_statistic

    def compute_statistic(self, data_list, statistic):
        if statistic == "mean":
            return np.mean(data_list)
        if statistic == "median":
            return np.median(data_list)
        if statistic == "sum":
            return np.sum(data_list)
        if statistic == "max":
            return np.max(data_list)
        if statistic == "min":
            return np.min(data_list)
        if statistic == "stdev":
            return np.std(data_list)

    def new_activity_dict(self):
        new_activity_dict = {}
        if self.parameters.calculate_frequency:
            new_activity_dict["frequency"] = 0
        if self.parameters.calculate_time:
            new_activity_dict["time"] = []
        if self.parameters.calculate_cost:
            new_activity_dict["cost"] = []
        return new_activity_dict

    def new_connection_dict(self):
        new_connection_dict = {}
        if self.parameters.calculate_frequency:
            new_connection_dict["frequency"] = 0
        if self.parameters.calculate_time:
            new_connection_dict["time"] = []
        return new_connection_dict

    def get_graph(self):
        return {"activities": self.activities, "connections": self.connections}

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
