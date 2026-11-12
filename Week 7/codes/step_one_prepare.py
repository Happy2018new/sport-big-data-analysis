import pandas as pd
from common import Config


def run_step_one() -> pd.Series:
    """筛选心率记录，用正则表达式提取时间和心率。"""
    raw = pd.read_csv(Config.ROOT / "dataofxiaomi.csv")
    values = raw.loc[raw["Key"] == "heart_rate", "Value"]
    df = pd.DataFrame()
    df["time"] = values.str.extract(r'"time"\s*:\s*(\d+)')[0]
    df["bpm"] = values.str.extract(r'"bpm"\s*:\s*(\d+)')[0]
    df = df.dropna().astype("int64")
    print(f"心率原始记录：{len(values)} 条；解析成功：{len(df)} 条")

    # 先解释为 UTC，再转换为北京时间，最后去掉时区标记。
    df["time"] = pd.to_datetime(df["time"], unit="s", utc=True)
    df["time"] = df["time"].dt.tz_convert("Asia/Shanghai").dt.tz_localize(None)
    df = df.sort_values("time").drop_duplicates("time")
    df.to_csv(Config.ROOT / "heart_rate_time_series.csv", index=False)
    print(
        f"去重后记录：{len(df)} 条；时间范围：{df['time'].min()} 至 {df['time'].max()}"
    )
    return df.set_index("time")["bpm"]


if __name__ == "__main__":
    run_step_one()
