import json
import pandas as pd
from common import Config


def extract_feature(raw: pd.DataFrame, key: str, field: str, sid: str) -> pd.DataFrame:
    """读取同一手环的某项记录，展开其中的时间和数值。"""
    selected = raw.query("Key == @key and Sid == @sid")
    data = pd.json_normalize(selected["Value"].map(json.loads))[["time", field]]
    data["time"] = pd.to_datetime(data["time"], unit="s", utc=True)
    data["time"] = data["time"].dt.tz_convert("Asia/Shanghai").dt.tz_localize(None)
    return data


def run_step_one() -> pd.DataFrame:
    """筛选手环记录，按相同时间配对步数和心率。"""
    raw = pd.read_csv(Config.DATA / "fitness_data.csv", dtype={"Sid": str})
    sources = pd.read_csv(Config.DATA / "data_source.csv", dtype={"Sid": str})
    sid = sources.loc[sources["Name"].str.strip() == "小米手环8", "Sid"].iloc[0]
    steps = extract_feature(raw, "steps", "steps", sid)
    heart = extract_feature(raw, "heart_rate", "bpm", sid)
    print(f"原始文件：{len(raw)}行、{len(raw.columns)}列")
    print(f"手环步数：{len(steps)}条；手环心率：{len(heart)}条")
    print(
        f"重复时间：步数{steps['time'].duplicated().sum()}条，"
        f"心率{heart['time'].duplicated().sum()}条"
    )

    # 只保留两项指标都有记录的分钟，缺失步数不补为零。
    steps = steps.drop_duplicates("time")
    heart = heart.drop_duplicates("time")
    data = steps.merge(heart, on="time", how="inner")
    clean = data.dropna().query("steps >= 0 and bpm > 0").sort_values("time")
    print(
        f"配对成功：{len(data)}条；缺失或非正心率、负步数剔除：{len(data) - len(clean)}条"
    )
    print(f"时间范围：{clean['time'].min()} 至 {clean['time'].max()}")
    return clean.reset_index(drop=True)
