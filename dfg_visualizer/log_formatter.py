import pandas as pd


# TODO: format log based on user column names
def log_formatter(log: pd.DataFrame, format: dict):
    log = log.rename(
        columns={
            format["case:concept:name"]: "case:concept:name",
            format["concept:name"]: "concept:name",
            format["time:timestamp"]: "time:timestamp",
            format["org:resource"]: "org:resource",
        }
    )

    if format["start_timestamp"] == "":
        log["start_timestamp"] = log[format["time:timestamp"]].copy()
    else:
        log = log.rename(columns={format["start_timestamp"]: "start_timestamp"})

    if format["cost:total"] == "":
        log["cost:total"] = 0
    else:
        log = log.rename(columns={format["cost:total"]: "cost:total"})

    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"], utc=True, format="mixed")
    log["start_timestamp"] = pd.to_datetime(log["start_timestamp"], utc=True, format="mixed")

    log["case:concept:name"] = log["case:concept:name"].astype(str)

    return log
