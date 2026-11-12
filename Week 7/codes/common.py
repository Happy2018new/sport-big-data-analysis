from pathlib import Path
import pandas as pd


class Config:
    ROOT: Path = Path(__file__).resolve().parent.parent
    FIGURES: Path = ROOT / "figures"
    DAY: str = "2024-05-10"


def load_heart_rate() -> pd.Series:
    """读取已转换的心率时间序列。"""
    df = pd.read_csv(Config.ROOT / "heart_rate_time_series.csv", parse_dates=["time"])
    return df.set_index("time")["bpm"]
