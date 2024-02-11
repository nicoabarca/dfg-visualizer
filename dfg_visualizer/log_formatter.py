import pandas as pd


def log_formatter(log: pd.DataFrame, format: dict):
    log = log.rename(
        columns={
            format["case:concept:name"]: "case:concept:name",
            format["concept:name"]: "concept:name",
            format["time:timestamp"]: "time:timestamp",
        }
    )

    if format["start_timestamp"] == "":
        log["start_timestamp"] = log["time:timestamp"].copy()
    else:
        log = log.rename(columns={format["start_timestamp"]: "start_timestamp"})

    if format["cost:total"] == "":
        log["cost:total"] = 0
    else:
        log = log.rename(columns={format["cost:total"]: "cost:total"})

    if format["org:resource"] == "":
        log["org:resoure"] = ""
    else:
        log = log.rename(columns={format["org:resource"]: "org:resource"})

    log["time:timestamp"] = pd.to_datetime(log["time:timestamp"], utc=True, format="mixed")
    log["start_timestamp"] = pd.to_datetime(log["start_timestamp"], utc=True, format="mixed")

    log["case:concept:name"] = log["case:concept:name"].astype(str)
    return log
