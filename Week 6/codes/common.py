import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


class Config:
    ROOT: Path = Path(__file__).resolve().parent
    FIGURES: Path = ROOT / "figures"
    FEATURES: list[str] = [f"Test_{number}" for number in range(1, 12)]
    TARGET: str = "Test_12"
    SEED: int = 42
    METRIC_COLUMNS: list[str] = [
        "模型",
        "特征数",
        "训练MSE",
        "训练RMSE",
        "训练R²",
        "测试MSE",
        "测试RMSE",
        "测试R²",
    ]


def load_data() -> pd.DataFrame:
    """加载数据"""
    Config.FIGURES.mkdir(exist_ok=True)
    return pd.read_csv(Config.ROOT / "student_marks.csv")


def split_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """数据集拆分"""
    df = load_data()
    return train_test_split(
        df[Config.FEATURES], df[Config.TARGET], test_size=0.2, random_state=Config.SEED
    )


def evaluate(y: pd.Series, prediction: np.ndarray) -> list[float]:
    """计算 MSE, RMSE 和 R²"""
    mse = mean_squared_error(y, prediction)
    return [mse, np.sqrt(mse), r2_score(y, prediction)]
