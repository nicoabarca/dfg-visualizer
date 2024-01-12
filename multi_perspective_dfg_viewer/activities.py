import pandas as pd


def get_start_activities(
    log: pd.DataFrame,
    case_id_key: str = "case:concept:name",
    activity_key: str = "concept:name",
):
    grouped_by_case_id = log.groupby(case_id_key, dropna=True, sort=False)
    start_activities = dict(grouped_by_case_id[activity_key].first().value_counts())
    return start_activities


def get_end_activities(
    log: pd.DataFrame,
    case_id_key: str = "case:concept:name",
    activity_key: str = "concept:name",
):
    grouped_by_case_id = log.groupby(case_id_key, dropna=True, sort=False)
    end_activities = dict(grouped_by_case_id[activity_key].last().value_counts())
    return end_activities
