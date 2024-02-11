def dimensions_min_and_max(activities, connections):
    activities_dimensions = next(iter(activities.values())).keys()
    connections_dimensions = next(iter(connections.values())).keys()
    dimensions_min_and_max = {key: (0, 0) for key in activities_dimensions}

    for dim in activities_dimensions:
        min_val = min((activity[dim] for activity in activities.values()))
        max_val = max((activity[dim] for activity in activities.values()))
        dimensions_min_and_max[dim] = (min_val, max_val)

    for dim in connections_dimensions:
        min_val = min((connection[dim] for connection in connections.values()))
        max_val = max((connection[dim] for connection in connections.values()))
        prev_min_val = dimensions_min_and_max[dim][0]
        prev_max_val = dimensions_min_and_max[dim][1]
        dimensions_min_and_max[dim] = (min(prev_min_val, min_val), max(prev_max_val, max_val))

    return dimensions_min_and_max


def ids_mapping(activities):
    id = 0
    mapping = {}
    for activity in activities.keys():
        mapping[activity] = f"A{id}"
        id += 1

    return mapping


def hsv_color(measure, dimension, dimension_scale):
    hue, saturation = hue_and_saturation_by_dimension(dimension)
    value_scale = (75, 35)
    value = round(interpolated_value(measure, dimension_scale, value_scale), 3)

    return f"{round(hue / 360, 3)} {round(saturation / 100, 3)} {round(value / 100, 3)}"


def hue_and_saturation_by_dimension(dimension):
    if dimension == "frequency":
        return (225, 100)  # blue
    elif dimension == "time":
        return (0, 100)  # red
    else:
        return (120, 100)  # green


def interpolated_value(measure, from_scale, to_scale):
    measure = max(min(measure, from_scale[1]), from_scale[0])
    denominator = max(1, (from_scale[1] - from_scale[0]))
    normalized_value = (measure - from_scale[0]) / denominator
    interpolated_value = to_scale[0] + normalized_value * (to_scale[1] - to_scale[0])
    return interpolated_value


def format_time(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    if hours > 0:
        return f"{hours} hr {minutes} min {remaining_seconds} seg"
    elif minutes > 0:
        return f"{minutes} min {remaining_seconds} seg"
    elif remaining_seconds > 0:
        return f"{remaining_seconds} seg"
    else:
        return "instant"


def link_width(measure, dimension_scale):
    width_scale = (1, 10)
    link_width = round(interpolated_value(measure, dimension_scale, width_scale), 2)
    return link_width
