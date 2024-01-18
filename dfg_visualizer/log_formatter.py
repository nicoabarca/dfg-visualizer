import pandas as pd


# TODO: format log based on user column names
def log_formatter(log: pd.DataFrame):
    log["Complete"] = pd.to_datetime(
        log["Complete"], utc=True, format="%Y-%m-%d %H:%M:%S"
    )

    log["Start"] = pd.to_datetime(log["Start"], utc=True, format="%Y-%m-%d %H:%M:%S")

    log = log.rename(
        columns={
            "Case ID": "case:concept:name",
            "Activity": "concept:name",
            "Complete": "time:timestamp",
            "Start": "start_timestamp",
            "Resource": "org:resource",
            "Cost": "cost:total",
        }
    )

    log["case:concept:name"] = log["case:concept:name"].astype(str)

    return log
