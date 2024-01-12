import pandas as pd
from copy import copy
from typing import Optional


def get_log_properties(
    log: pd.DataFrame,
    activity_key: str = "concept:name",
    timestamp_key: str = "time:timestamp",
    case_id_key: str = "case:concept:name",
    resource_key: str = "org:resource",
    group_key: Optional[str] = None,
    start_timestamp_key: Optional[str] = None,
    **kwargs
) -> dict:
    log_properties = {}

    if not isinstance(log, pd.DataFrame):
        return {}

    print(activity_key, timestamp_key, case_id_key, resource_key)

    # if activity_key is not None:
    #     parameters[constants.PARAMETER_CONSTANT_ACTIVITY_KEY] = activity_key
    #     parameters[constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY] = activity_key

    # if timestamp_key is not None:
    #     parameters[constants.PARAMETER_CONSTANT_TIMESTAMP_KEY] = timestamp_key

    # if start_timestamp_key is not None:
    #     parameters[
    #         constants.PARAMETER_CONSTANT_START_TIMESTAMP_KEY
    #     ] = start_timestamp_key

    # if case_id_key is not None:
    #     parameters[constants.PARAMETER_CONSTANT_CASEID_KEY] = case_id_key

    # if resource_key is not None:
    #     parameters[constants.PARAMETER_CONSTANT_RESOURCE_KEY] = resource_key

    # if group_key is not None:
    #     parameters[constants.PARAMETER_CONSTANT_GROUP_KEY] = group_key

    # for k, v in kwargs.items():
    #     parameters[k] = v

    return log_properties
