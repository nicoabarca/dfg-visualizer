import pandas as pd

QUANTITY_OF_CASES = 655


def get_multi_perspective_dfg(
    log: pd.DataFrame,
    case_id_key: str = "case:concept:name",
    activity_key: str = "concept:name",
    timestamp_key: str = "time:timestamp",
    start_timestamp_key: str = "start_timestamp",
    cost_key: str = "cost:total",
    calculate_frequency: bool = True,
    calculate_time_performance: bool = True,
    calculate_cost_performance: bool = True,
    frequency_measure: str = "absolute-activity",  # absolute-case, relative-activity, relative-case
    time_measure: str = "mean",  # mean, median, sum, max, min, stdev
    cost_measure: str = "mean",  # mean, median, sum, max, min, stdev
):
    multi_perspective_dfg = {"activities": {}, "connections": {}}
    activities = multi_perspective_dfg["activities"]
    connections = multi_perspective_dfg["connections"]

    grouped_by_case_id = log.groupby(case_id_key, dropna=True)

    # FIXME: this approach is for case time_measure=mean, cost_measure=mean, frecuency=absolute_activity

    for _, group_data in grouped_by_case_id:
        rows_quantity = group_data.shape[0]
        for index in range(rows_quantity):
            prev_row = group_data.iloc[index - 1] if index > 0 else None
            actual_row = group_data.iloc[index]

            actual_activity_name = actual_row[activity_key]
            actual_time_cost = (
                actual_row[timestamp_key] - actual_row[start_timestamp_key]
            )
            actual_money_cost = actual_row[cost_key]

            # Adding activity to activities dictionary
            if actual_activity_name in activities:
                activities[actual_activity_name]["frequency"] += 1
                activities[actual_activity_name]["time"] += (
                    actual_time_cost / QUANTITY_OF_CASES
                )
                activities[actual_activity_name]["cost"] += (
                    actual_money_cost / QUANTITY_OF_CASES
                )
            else:
                activities[actual_activity_name] = {
                    "frequency": 1,
                    "time": actual_time_cost,
                    "cost": actual_money_cost,
                }

            # Adding connection to connections dictionary
            if prev_row is not None:
                prev_activity_name = prev_row[activity_key]

                time_between_activities = (
                    actual_row[start_timestamp_key] - prev_row[timestamp_key]
                )

                actual_connection = (prev_activity_name, actual_activity_name)

                if actual_connection in connections:
                    connections[actual_connection]["frequency"] += 1
                    connections[actual_connection]["time"] += (
                        time_between_activities / QUANTITY_OF_CASES
                    )
                else:
                    connections[actual_connection] = {
                        "frequency": 1,
                        "time": time_between_activities,
                    }

    return multi_perspective_dfg
