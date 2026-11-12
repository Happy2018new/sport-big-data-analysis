from pathlib import Path
from typing import Any
import matplotlib.pyplot as plt
import pandas as pd
from common import Config


class PlotConfig:
    STYLE: dict[str, Any] = {
        "font.family": ["Latin Modern Math", "SimSun"],
        "mathtext.fontset": "cm",
        "axes.formatter.use_mathtext": True,
        "axes.unicode_minus": False,
        "svg.fonttype": "path",
        "font.size": 11,
    }
    COLORS: list[str] = ["#497f72", "#c87c53", "#697da0", "#98759a", "#b4a15b"]


plt.rcParams.update(PlotConfig.STYLE)


def save_figure(path: Path) -> None:
    """保存当前图为SVG。"""
    path.parent.mkdir(exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, format="svg", bbox_inches="tight")
    plt.close()


def set_health_axis(ax: plt.Axes) -> None:
    """统一二维健康散点图的坐标。"""
    ax.set_xlabel("该分钟记录步数（步）")
    ax.set_ylabel("同时刻心率（bpm）")
    ax.set_xlim(-3, 130)
    ax.set_ylim(50, 155)
    ax.grid(alpha=0.15)


def plot_original(data: pd.DataFrame) -> None:
    """展示聚类前的两个指标。"""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(
        data["steps"],
        data["bpm"],
        s=13,
        alpha=0.35,
        color=PlotConfig.COLORS[0],
        edgecolors="none",
    )
    set_health_axis(ax)
    ax.set_title("同一分钟步数与心率的分布")
    save_figure(Config.FIGURES / "01二维健康数据.svg")


def plot_selection(quality: pd.DataFrame) -> None:
    """用簇内平方和及轮廓系数比较簇数。"""
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))
    for ax, field, title, color in zip(
        axes,
        ["sse", "silhouette"],
        ["簇内平方和（SSE）", "轮廓系数"],
        PlotConfig.COLORS,
    ):
        ax.plot(quality["k"], quality[field], "o-", color=color)
        ax.set_xticks(quality["k"])
        ax.set_xlabel("簇数 k")
        ax.set_ylabel(title)
        ax.set_title(title)
        ax.grid(alpha=0.2)
    save_figure(Config.FIGURES / "02聚类簇数选择.svg")


def plot_clusters(result: pd.DataFrame, centers: pd.DataFrame) -> None:
    """在原始单位下显示聚类结果和中心。"""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for group, part in result.groupby("cluster"):
        ax.scatter(
            part["steps"],
            part["bpm"],
            s=13,
            alpha=0.45,
            color=PlotConfig.COLORS[group - 1],
            edgecolors="none",
            label=f"簇{group}（{len(part)}条）",
        )
    ax.scatter(
        centers["steps"],
        centers["bpm"],
        marker="X",
        s=130,
        color="black",
        edgecolors="white",
        linewidths=0.8,
        label="聚类中心",
    )
    set_health_axis(ax)
    ax.set_title("K-means聚类结果（K-means++初始化）")
    ax.legend(loc="upper left", fontsize=10)
    save_figure(Config.FIGURES / "03二维健康数据聚类.svg")
