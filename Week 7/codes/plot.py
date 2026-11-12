from pathlib import Path
from typing import Any

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


class PlotConfig:
    STYLE: dict[str, Any] = {
        "font.family": ["Latin Modern Math", "SimSun"],
        "mathtext.fontset": "cm",
        "axes.formatter.use_mathtext": True,
        "axes.unicode_minus": False,
        "svg.fonttype": "path",
        "font.size": 11,
    }
    COLORS: list[str] = ["#497f72", "#c87c53", "#697da0"]


plt.rcParams.update(PlotConfig.STYLE)


def save_figure(output_path: Path) -> None:
    """保存当前图片"""
    output_path.parent.mkdir(exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, format="svg", bbox_inches="tight")
    plt.close()


def set_day_axis(ax: plt.Axes, day: pd.Series) -> None:
    """统一单日图的小时刻度"""
    start = day.index[0].normalize()
    ax.set_xlim(start, start + pd.Timedelta(days=1))
    ax.set_xticks(pd.date_range(start, periods=9, freq="3h"))
    ax.set_xticklabels([f"{hour:02d}:00" for hour in range(0, 25, 3)])
    ax.set_xlabel("北京时间（小时）")
    ax.set_ylabel("心率（bpm）")
    ax.grid(alpha=0.2)


def plot_overview(heart: pd.Series, output_dir: Path) -> None:
    """用折线图、直方图和箱线图观察整体情况"""
    plt.figure(figsize=(10, 3.9))
    # 补出一分钟时间索引，缺测处保持空白，避免跨缺口连线。
    timeline = heart.asfreq("1min")
    plt.plot(timeline.index, timeline, color=PlotConfig.COLORS[0], lw=0.7)
    gaps = heart.index.to_series().diff()
    gap_end = gaps.idxmax()
    gap_start = gap_end - gaps.max()
    plt.axvspan(gap_start, gap_end, color="#eeeeee")
    plt.text(gap_start + gaps.max() / 2, 150, "最长缺测段", ha="center")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    plt.xlabel("日期（北京时间）")
    plt.ylabel("心率（bpm）")
    plt.title("全时段心率变化（空白表示缺测）")
    save_figure(output_dir / "01全时段心率.svg")

    plt.figure(figsize=(8, 4))
    plt.hist(
        heart, bins=range(30, 181, 5), color=PlotConfig.COLORS[0], edgecolor="white"
    )
    plt.axvline(
        heart.median(),
        color=PlotConfig.COLORS[1],
        ls="--",
        label=f"中位数 {heart.median():.0f} bpm",
    )
    plt.xlabel("心率（bpm）")
    plt.ylabel("记录数（条）")
    plt.title("心率数值分布")
    plt.legend()
    save_figure(output_dir / "02心率分布.svg")

    plt.figure(figsize=(8, 2.6))
    plt.boxplot(heart, vert=False, widths=0.45)
    plt.yticks([1], ["全部记录"])
    plt.xlabel("心率（bpm）")
    plt.title("心率箱线图（按 1.5 IQR 标记离群点）")
    save_figure(output_dir / "03心率箱线图.svg")


def plot_daily(day: pd.Series, output_dir: Path) -> None:
    """观察五月十日的日内变化"""
    fig, ax = plt.subplots(figsize=(10, 4))
    series = day.asfreq("1min")
    ax.plot(series.index, series, color=PlotConfig.COLORS[0], lw=0.9)
    for time, label, offset in [(day.idxmin(), "最低", -20), (day.idxmax(), "最高", 8)]:
        ax.scatter(time, day[time], color=PlotConfig.COLORS[1], zorder=3)
        ax.annotate(
            f"{label} {day[time]:.0f} bpm（{time:%H:%M}）",
            (time, day[time]),
            xytext=(7, offset),
            textcoords="offset points",
            fontsize=9,
        )
    end = day.index[0].normalize() + pd.Timedelta(days=1)
    ax.axvspan(day.index[-1], end, color="#eeeeee")
    ax.text(
        day.index[-1] + (end - day.index[-1]) / 2,
        day.mean(),
        "此后无记录",
        ha="center",
        fontsize=10,
    )
    ax.set_ylim(day.min() - 10, day.max() + 10)
    set_day_axis(ax, day)
    ax.set_title("2024年5月10日心率变化")
    save_figure(output_dir / "04单日心率.svg")


def plot_resampling(
    day: pd.Series,
    aggregation: pd.DataFrame,
    strategies: pd.DataFrame,
    output_dir: Path,
) -> None:
    """比较十分钟重采样、聚合函数及缺失值处理"""
    fig, ax = plt.subplots(figsize=(10, 4))
    original = day.asfreq("1min")
    ax.plot(original.index, original, color="#aeb7b3", lw=0.7, label="原始心率")
    ax.plot(
        aggregation.index,
        aggregation["mean"],
        color=PlotConfig.COLORS[0],
        lw=1.5,
        label="10分钟均值",
    )
    set_day_axis(ax, day)
    ax.legend()
    ax.set_title("原始心率与10分钟重采样均值")
    save_figure(output_dir / "05重采样均值.svg")

    fig, axes = plt.subplots(2, 1, figsize=(10, 6.4), sharex=True)
    for column, name, color in zip(
        ["mean", "median", "max"], ["均值", "中位数", "最大值"], PlotConfig.COLORS
    ):
        axes[0].plot(
            aggregation.index, aggregation[column], label=name, color=color, lw=1.2
        )
    axes[0].set_title("10分钟窗口的心率水平")
    axes[0].legend(ncol=3)
    axes[1].plot(
        aggregation.index, aggregation["std"], color=PlotConfig.COLORS[0], lw=1.2
    )
    axes[1].set_title("10分钟窗口内的标准差")
    for ax in axes:
        set_day_axis(ax, day)
    axes[0].set_xlabel("")
    axes[1].set_ylabel("心率标准差（bpm）")
    save_figure(output_dir / "06聚合函数比较.svg")

    fig, ax = plt.subplots(figsize=(10, 4))
    for column, color, style in zip(
        strategies.columns, PlotConfig.COLORS, ["-", "--", ":"]
    ):
        ax.plot(
            strategies.index,
            strategies[column],
            color=color,
            linestyle=style,
            lw=1.3,
            label=column,
        )
    set_day_axis(ax, day)
    ax.set_title("缺失处理比较（117个窗口均有观测，三条曲线重合）")
    ax.legend(ncol=3)
    save_figure(output_dir / "07缺失窗口处理.svg")


def plot_rolling(day: pd.Series, rolling: pd.DataFrame, output_dir: Path) -> None:
    """比较后向和居中的三十分钟滑动平均"""
    fig, ax = plt.subplots(figsize=(10, 4))
    original = day.asfreq("1min")
    ax.plot(original.index, original, color="#b5bcb9", lw=0.7, label="原始心率")
    for column, color in zip(rolling.columns, PlotConfig.COLORS):
        line = rolling[column].asfreq("1min")
        ax.plot(line.index, line, color=color, lw=1.5, label=f"30分钟{column}")
    set_day_axis(ax, day)
    ax.set_title("30分钟后向与中心滑动平均")
    ax.legend(ncol=3, fontsize=9)
    save_figure(output_dir / "08滑动平均.svg")


def plot_levels(heart: pd.Series, output_dir: Path) -> None:
    """用心率水平构成补充整体观察，不作为活动强度诊断"""
    counts = pd.cut(
        heart,
        [-float("inf"), 59, 100, float("inf")],
        labels=["低于60 bpm", "60～100 bpm", "高于100 bpm"],
    )
    plt.figure(figsize=(7, 4.3))
    plt.pie(
        counts.value_counts(sort=False),
        labels=counts.cat.categories,
        autopct="%1.1f%%",
        startangle=90,
        colors=PlotConfig.COLORS,
        wedgeprops={"edgecolor": "white"},
        pctdistance=0.7,
    )
    plt.title("已观测记录的心率水平构成")
    save_figure(output_dir / "09心率水平构成.svg")
