import re


def get_dimensions_min_and_max(activities, connections):
    min_cost_in_activities = min(activity["cost"] for activity in activities.values())
    max_cost_in_activities = max(activity["cost"] for activity in activities.values())

    min_time_in_activities = min(activity["time"] for activity in activities.values())
    max_time_in_activities = max(activity["time"] for activity in activities.values())

    min_freq_in_activities = min(
        activity["frequency"] for activity in activities.values()
    )
    max_freq_in_activities = max(
        activity["frequency"] for activity in activities.values()
    )

    min_freq_in_connections = min(
        connection["frequency"] for connection in connections.values()
    )
    max_freq_in_connections = max(
        connection["frequency"] for connection in connections.values()
    )

    min_time_in_connections = min(
        connection["time"] for connection in connections.values()
    )
    max_time_in_connections = max(
        connection["time"] for connection in connections.values()
    )

    min_cost, max_cost = min_cost_in_activities, max_cost_in_activities
    min_time, max_time = min(min_time_in_activities, min_time_in_connections), max(
        max_time_in_activities, max_time_in_connections
    )
    min_freq, max_freq = min(min_freq_in_activities, min_freq_in_connections), max(
        max_freq_in_activities, max_freq_in_connections
    )

    return {
        "frequency": (min_freq, max_freq),
        "time": (min_time, max_time),
        "cost": (min_cost, max_cost),
    }


def hsl_interpolation_color(val, dimension, dimension_scale):
    hue = 0
    saturation = 0
    l_scale = (75, 35)
    if dimension == "frequency":
        hue = 225
        saturation = 100
    elif dimension == "time":
        hue = 0
        saturation = 100
    elif dimension == "cost":
        hue = 120
        saturation = 60

    normalized_value = (val - dimension_scale[0]) / (
        dimension_scale[1] - dimension_scale[0]
    )

    lightness = l_scale[0] + normalized_value * (l_scale[1] - l_scale[0])

    return f"hsl({hue},{saturation}%,{lightness}%)"


def link_width(val, dimension_scale):
    width_scale = (0.1, 5)
    normalized_value = (val - dimension_scale[0]) / (
        dimension_scale[1] - dimension_scale[0]
    )

    width = width_scale[0] + normalized_value * (width_scale[1] - width_scale[0])

    return width


def text_color(background_color):
    background_lightness = (
        re.search(r"hsl\(\d+,\d+%,(\d+\.?\d*%?)\)", background_color)
        .group(1)
        .replace("%", "")
    )

    threshold = 55
    if float(background_lightness) > threshold:
        return "black"
    else:
        return "white"


def format_time(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    if hours > 0:
        return f"{hours} hr, {minutes} min, {remaining_seconds} seg"
    elif minutes > 0:
        return f"{minutes} min, {remaining_seconds} seg"
    else:
        return f"{remaining_seconds} seg"
