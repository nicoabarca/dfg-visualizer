def get_dimensions_min_and_max(activities, connections):
    min_cost_in_activities = min((activity["cost"] for activity in activities.values()))
    max_cost_in_activities = max((activity["cost"] for activity in activities.values()))

    min_time_in_activities = min((activity["time"] for activity in activities.values()))
    max_time_in_activities = max((activity["time"] for activity in activities.values()))

    min_freq_in_activities = min((activity["frequency"] for activity in activities.values()))
    max_freq_in_activities = max((activity["frequency"] for activity in activities.values()))

    min_freq_in_connections = min((connection["frequency"] for connection in connections.values()))
    max_freq_in_connections = max((connection["frequency"] for connection in connections.values()))

    min_time_in_connections = min((connection["time"] for connection in connections.values()))
    max_time_in_connections = max((connection["time"] for connection in connections.values()))

    min_cost, max_cost = min_cost_in_activities, max_cost_in_activities
    min_time, max_time = (
        min(min_time_in_activities, min_time_in_connections),
        max(max_time_in_activities, max_time_in_connections),
    )
    min_freq, max_freq = (
        min(min_freq_in_activities, min_freq_in_connections),
        max(max_freq_in_activities, max_freq_in_connections),
    )

    return {
        "frequency": (min_freq, max_freq),
        "time": (min_time, max_time),
        "cost": (min_cost, max_cost),
    }


def hsl_color(measure, dimension, dimension_scale):
    hue = 0
    saturation = 0
    lightness_scale = (75, 35)
    if dimension == "frequency":  # blue
        hue = 225
        saturation = 100
    elif dimension == "time":  # red
        hue = 0
        saturation = 100
    elif dimension == "cost":  # green
        hue = 120
        saturation = 60

    lightness = round(interpolated_value(measure, dimension_scale, lightness_scale), 2)

    return f"hsl({hue},{saturation}%,{lightness}%)"


def link_width(measure, dimension_scale):
    width_scale = (0.1, 8)
    link_width = round(interpolated_value(measure, dimension_scale, width_scale), 2)
    return link_width


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


def interpolated_value(measure, from_scale, to_scale):
    measure = max(min(measure, from_scale[1]), from_scale[0])
    denominator = max(1, (from_scale[1] - from_scale[0]))
    normalized_value = (measure - from_scale[0]) / denominator
    interpolated_value = to_scale[0] + normalized_value * (to_scale[1] - to_scale[0])
    return interpolated_value


def activities_id_mapping(activities):
    id = 0
    mapping = {}
    for activity in activities.keys():
        mapping[activity] = id
        id += 1

    return mapping
