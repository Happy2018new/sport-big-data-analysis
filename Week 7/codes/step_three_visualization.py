import pandas as pd
from common import Config, load_heart_rate
from plot import plot_overview, plot_levels


def run_step_three(heart: pd.Series) -> None:
    """从趋势、分布、离散程度和构成四个角度观察心率。"""
    Config.FIGURES.mkdir(exist_ok=True)
    plot_overview(heart, Config.FIGURES)
    plot_levels(heart, Config.FIGURES)


if __name__ == "__main__":
    run_step_three(load_heart_rate())
