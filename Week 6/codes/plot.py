import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Any
from scipy import stats
from pathlib import Path


class PlotConfig:
    STYLE: dict[str, Any] = {
        "font.family": ["Latin Modern Math", "SimSun"],
        "mathtext.fontset": "cm",
        "axes.formatter.use_mathtext": True,
        "axes.unicode_minus": False,
        "svg.fonttype": "path",
    }
    TRAIN_COLOR: str = "#497f72"
    TEST_COLOR: str = "#c87c53"


def plot_correlation(correlation: pd.DataFrame, output_path: Path) -> None:
    """展示十二次考试成绩之间的相关性"""
    with plt.rc_context(PlotConfig.STYLE):
        plt.figure(figsize=(10, 9))
        plt.imshow(correlation, cmap="RdBu_r", vmin=-1, vmax=1)
        plt.colorbar(label="相关系数", fraction=0.046, pad=0.04)
        positions = range(len(correlation))
        plt.xticks(positions, correlation.columns, rotation=45, ha="right")
        plt.yticks(positions, correlation.columns)
        for row in positions:
            for column in positions:
                value = correlation.iloc[row, column]
                color = "white" if abs(value) >= 0.6 else "black"
                plt.text(
                    column,
                    row,
                    f"{value:.2f}",
                    ha="center",
                    va="center",
                    fontsize=8,
                    color=color,
                )
        plt.title("十二次考试成绩相关系数热力图", pad=14)
        plt.tight_layout()
        plt.savefig(output_path, format="svg", bbox_inches="tight")
        plt.close()


def plot_predictions(
    y_train: pd.Series,
    y_test: pd.Series,
    train_prediction: np.ndarray,
    test_prediction: np.ndarray,
    output_path: Path,
) -> None:
    """区分训练和测试记录，观察多元回归的预测误差"""
    limit = max(100, train_prediction.max(), test_prediction.max()) + 3
    with plt.rc_context(PlotConfig.STYLE):
        plt.figure(figsize=(8, 7))
        plt.scatter(
            y_train,
            train_prediction,
            color=PlotConfig.TRAIN_COLOR,
            alpha=0.75,
            s=38,
            label="训练集",
        )
        plt.scatter(
            y_test,
            test_prediction,
            color=PlotConfig.TEST_COLOR,
            marker="^",
            s=55,
            label="测试集",
        )
        plt.plot(
            [0, limit], [0, limit], "--", color="#555555", label="预测值等于真实值"
        )
        plt.xlim(0, limit)
        plt.ylim(0, limit)
        plt.xlabel("真实成绩（分）")
        plt.ylabel("预测成绩（分）")
        plt.title("全部特征回归的预测值与真实值")
        plt.legend()
        plt.grid(alpha=0.25)
        plt.gca().set_aspect("equal")
        plt.tight_layout()
        plt.savefig(output_path, format="svg", bbox_inches="tight")
        plt.close()


def plot_residuals(
    y_train: pd.Series,
    y_test: pd.Series,
    train_prediction: np.ndarray,
    test_prediction: np.ndarray,
    output_path: Path,
) -> None:
    """用残差散点图与正态 Q-Q 图检查训练和测试误差"""
    groups = [
        (
            "训练集",
            y_train - train_prediction,
            train_prediction,
            PlotConfig.TRAIN_COLOR,
        ),
        ("测试集", y_test - test_prediction, test_prediction, PlotConfig.TEST_COLOR),
    ]
    with plt.rc_context(PlotConfig.STYLE):
        plt.figure(figsize=(11, 8))
        for index, (name, residual, prediction, color) in enumerate(groups):
            plt.subplot(2, 2, index * 2 + 1)
            plt.scatter(prediction, residual, color=color, s=35, alpha=0.8)
            plt.axhline(0, color="#555555", linestyle="--")
            plt.title(f"{name}残差与拟合值")
            plt.xlabel("拟合成绩（分）")
            plt.ylabel("残差（分）")
            plt.grid(alpha=0.25)
            plt.subplot(2, 2, index * 2 + 2)
            (theoretical, ordered), (slope, intercept, _) = stats.probplot(
                residual, dist="norm"
            )
            plt.scatter(theoretical, ordered, color=color, s=30)
            plt.plot(theoretical, slope * theoretical + intercept, color="#555555")
            plt.title(f"{name}残差正态 Q-Q 图")
            plt.xlabel("理论正态分位数")
            plt.ylabel("残差有序值（分）")
            plt.grid(alpha=0.25)
        plt.tight_layout()
        plt.savefig(output_path, format="svg", bbox_inches="tight")
        plt.close()


y_train: np.ndarray = []
train_prediction: np.ndarray = []
