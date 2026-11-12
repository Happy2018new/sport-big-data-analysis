from typing import Any

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.graphics.gofplots import qqplot
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from common import Config


class PlotConfig:
    STYLE: dict[str, Any] = {
        "font.family": ["Latin Modern Math", "SimSun"],
        "mathtext.fontset": "cm",
        "axes.formatter.use_mathtext": True,
        "axes.unicode_minus": False,
        "svg.fonttype": "path",
        "font.size": 14,
    }
    COLORS: list[str] = ["#497f72", "#c87c53", "#697da0"]


plt.rcParams.update(PlotConfig.STYLE)


def save_figure(name: str) -> None:
    Config.FIGURES.mkdir(exist_ok=True)
    plt.tight_layout()
    plt.savefig(Config.FIGURES / name, format="svg", bbox_inches="tight")
    plt.close()


def plot_overview(close: pd.Series) -> None:
    """查看训练、测试及未使用部分的收盘价"""
    fig, ax = plt.subplots(figsize=(10, 4))
    for series, name, color in zip(
        [close.loc[:"2019"], close.loc["2020"], close.loc["2021":]],
        ["训练集（2000—2019年）", "测试集（2020年）", "未使用（2021年）"],
        PlotConfig.COLORS,
    ):
        ax.plot(series.index, series, color=color, lw=0.9, label=name)
    ax.set(title="收盘价全景与数据划分", xlabel="日期", ylabel="收盘价")
    ax.legend(loc="upper left")
    ax.grid(alpha=0.2)
    save_figure("01收盘价全景.svg")


def plot_differences(train: pd.Series) -> None:
    """比较原始价格与两种差分结果"""
    fig, axes = plt.subplots(3, 1, figsize=(10, 7), sharex=True)
    series_list = [train, train.diff().dropna(), train.diff().diff().dropna()]
    for ax, series, title, color in zip(
        axes, series_list, ["原始收盘价", "一阶差分", "二阶差分"], PlotConfig.COLORS
    ):
        ax.plot(series.index, series, color=color, lw=0.7)
        ax.set_title(title)
        ax.set_ylabel("数值")
        ax.grid(alpha=0.2)
    axes[-1].set_xlabel("训练集日期")
    save_figure("02差分与平稳性.svg")


def plot_correlations(difference: pd.Series) -> None:
    """只用训练集的一阶差分查看前 30 阶相关性"""
    fig, axes = plt.subplots(2, 1, figsize=(9, 6))
    plot_acf(difference, lags=30, zero=False, ax=axes[0], title="一阶差分的 ACF")
    plot_pacf(
        difference,
        lags=30,
        zero=False,
        method="ywm",
        ax=axes[1],
        title="一阶差分的 PACF",
    )
    for ax in axes:
        ax.set(xlabel="滞后阶数（交易日）", ylabel="相关系数")
        ax.set_ylim(-0.10, 0.10)
        ax.grid(alpha=0.2)
    save_figure("03一阶差分相关图.svg")


def plot_residuals(residuals: pd.Series) -> None:
    """检查残差的变化，自相关和正态分布偏离情况"""
    fig, axes = plt.subplots(3, 1, figsize=(9, 8.6))
    axes[0].plot(residuals.to_numpy(), color=PlotConfig.COLORS[0], lw=0.6)
    axes[0].axhline(0, color="gray", lw=0.7)
    axes[0].set(title="模型残差", xlabel="训练集交易日序号", ylabel="残差")
    plot_acf(residuals, lags=30, zero=False, ax=axes[1], title="残差 ACF")
    axes[1].set(xlabel="滞后阶数（交易日）", ylabel="相关系数")
    axes[1].set_ylim(-0.10, 0.10)
    qqplot(residuals, line="s", ax=axes[2], marker=".", markersize=2)
    axes[2].set(title="残差正态 Q-Q 图", xlabel="理论正态分位数", ylabel="残差分位数")
    for ax in axes:
        ax.grid(alpha=0.2)
    save_figure("04模型残差诊断.svg")


def set_test_axis(ax: plt.Axes) -> None:
    """统一 2020 年预测图的日期刻度"""
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    ax.set(xlabel="2020年日期", ylabel="收盘价")
    ax.grid(alpha=0.2)


def plot_forecast(
    train: pd.Series,
    test: pd.Series,
    predictions: pd.DataFrame,
    interval: pd.DataFrame,
) -> None:
    """比较一次全年预测与基线模型"""
    fig, axes = plt.subplots(2, 1, figsize=(10, 6.5), sharex=True)
    actual = pd.concat([train.tail(1), test])
    for ax in axes:
        ax.plot(
            actual.index, actual, color=PlotConfig.COLORS[0], lw=1, label="实际收盘价"
        )
        set_test_axis(ax)
    axes[0].plot(
        test.index,
        predictions["ARIMA一次预测"],
        color=PlotConfig.COLORS[1],
        lw=1.3,
        label="ARIMA一次预测252步",
    )
    axes[0].fill_between(
        test.index,
        interval.iloc[:, 0],
        interval.iloc[:, 1],
        color=PlotConfig.COLORS[1],
        alpha=0.15,
        label="95%预测区间",
    )
    axes[0].set_title("固定在2019年末预测2020年")
    axes[0].set_xlabel("")
    axes[1].plot(
        test.index,
        predictions["Naive逐日预测"],
        color=PlotConfig.COLORS[2],
        lw=0.9,
        ls="--",
        label="Naive逐日预测",
    )
    axes[1].plot(
        test.index,
        predictions["训练均值"],
        color=PlotConfig.COLORS[1],
        lw=1.1,
        ls=":",
        label="训练集均值",
    )
    axes[1].set_title("逐日 Naive 与训练均值基线")
    for ax in axes:
        ax.legend(loc="upper left", ncol=3, fontsize=13)
    save_figure("05全年预测比较.svg")


def plot_rolling(test: pd.Series, rolling: pd.Series, naive: pd.Series) -> None:
    """在相同的逐日预测条件下比较两种方法"""
    fig, axes = plt.subplots(2, 1, figsize=(10, 6))
    # 全年图观察整体变化，前 30 个交易日放大查看相近的预测
    for ax, count, title in zip(
        axes, [len(test), 30], ["2020年逐日预测", "前30个交易日放大"]
    ):
        for series, name, color, style in zip(
            [test, rolling, naive],
            ["实际收盘价", "ARIMA逐日预测", "Naive逐日预测"],
            PlotConfig.COLORS,
            ["-", "--", ":"],
        ):
            ax.plot(
                test.index[:count],
                series.iloc[:count],
                color=color,
                ls=style,
                lw=1,
                label=name,
            )
        ax.set(title=title, xlabel="2020年日期", ylabel="收盘价")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
        ax.grid(alpha=0.2)
        ax.legend(ncol=3, fontsize=13)
    save_figure("06逐日预测比较.svg")
