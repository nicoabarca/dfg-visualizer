def new_activity_dict(params):
    new_activity_dict = {}
    if params.calculate_frequency:
        new_activity_dict["frequency"] = 0
    if params.calculate_time:
        new_activity_dict["time"] = []
    if params.calculate_cost:
        new_activity_dict["cost"] = []
    return new_activity_dict


def new_connection_dict(params):
    new_connection_dict = {}
    if params.calculate_frequency:
        new_connection_dict["frequency"] = 0
    if params.calculate_time:
        new_connection_dict["time"] = []
    return new_connection_dict
