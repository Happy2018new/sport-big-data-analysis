from pathlib import Path
import pandas as pd


class Config:
    ROOT: Path = Path(__file__).resolve().parent.parent
    FIGURES: Path = ROOT / "figures"
    SEED: int = 42


def load_close() -> pd.Series:
    """按交易日顺序读取收盘价"""
    data = pd.read_csv(Config.ROOT / "TATASTEEL.csv", parse_dates=["Date"])
    return data.sort_values("Date").set_index("Date")["Close"]
