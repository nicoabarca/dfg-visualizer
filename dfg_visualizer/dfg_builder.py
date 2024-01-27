import numpy as np


class DirectlyFollowsGraphBuilder:
    def __init__(self, dfg, log, parameters):
        self.dfg = dfg
        self.log = log
        self.parameters = parameters

    def start(self):
        grouped_cases_by_id = self.log.groupby(
            self.parameters.case_id_key, dropna=True, sort=False
        )
        self.create_graph(grouped_cases_by_id)

    def create_graph(self, grouped_cases_by_id):
        self.get_start_and_end_activities(grouped_cases_by_id)

        for _, group_data in grouped_cases_by_id:
            self.update_graph(group_data)

        self.compute_graph_dimensions_statistics()

    def get_start_and_end_activities(self, grouped_cases_by_id):
        self.dfg.start_activities = dict(
            grouped_cases_by_id[self.parameters.activity_key].first().value_counts()
        )

        self.dfg.end_activities = dict(
            grouped_cases_by_id[self.parameters.activity_key].last().value_counts()
        )

    def update_graph(self, group_data):
        group_data_rows_quantity = group_data.shape[0]
        for index in range(group_data_rows_quantity):
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
        if name not in self.dfg.activities.keys():
            self.dfg.activities[name] = self.new_activity_dict()
        if self.parameters.calculate_frequency:
            self.dfg.activities[name]["frequency"] += 1
        if self.parameters.calculate_time:
            self.dfg.activities[name]["time"].append(time.total_seconds())
        if self.parameters.calculate_cost:
            self.dfg.activities[name]["cost"].append(cost)

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
        if name not in self.dfg.connections.keys():
            self.dfg.connections[name] = self.new_connection_dict()
        if self.parameters.calculate_frequency:
            self.dfg.connections[name]["frequency"] += 1
        if self.parameters.calculate_time:
            self.dfg.connections[name]["time"].append(
                time_between_activities.total_seconds()
            )

    def compute_graph_dimensions_statistics(self):
        for activity_name, dimensions in self.dfg.activities.items():
            for dimension in dimensions.keys():
                if dimension != "frequency":
                    activity_dimension_data = self.dfg.activities[activity_name][
                        dimension
                    ]
                    dimension_statistic = self.get_dimension_statistic(dimension)
                    self.dfg.activities[activity_name][
                        dimension
                    ] = self.compute_statistic(
                        activity_dimension_data, dimension_statistic
                    )
        for connection_name, dimensions in self.dfg.connections.items():
            for dimension in dimensions.keys():
                if dimension != "frequency":
                    connection_dimension_data = self.dfg.connections[connection_name][
                        dimension
                    ]
                    dimension_statistic = self.get_dimension_statistic(dimension)
                    self.dfg.connections[connection_name][
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
