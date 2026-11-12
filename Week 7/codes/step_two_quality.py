import pandas as pd
from common import load_heart_rate


def run_step_two(heart: pd.Series) -> None:
    """检查采样间隔、长缺口、描述统计和异常值，不删除观测。"""
    print("\n二、数据质量体检")
    print(
        f"有效记录：{len(heart)} 条；有记录日期：{heart.index.normalize().nunique()} 天"
    )
    print(f"起止时间：{heart.index.min()} 至 {heart.index.max()}")
    span = heart.index.max() - heart.index.min()
    print(
        f"时间跨度：{span.days} 天 {span.components.hours} 小时 {span.components.minutes} 分钟"
    )
    interval = heart.index.to_series().diff().dt.total_seconds().div(60)
    frequency = interval.value_counts().sort_index().to_frame("次数")
    frequency["占比（%）"] = frequency["次数"] / interval.count() * 100
    frequency.index.name = "采样间隔（分钟）"
    print("采样间隔分布：\n" + frequency.round(3).to_string())

    gaps = pd.DataFrame(
        {
            "开始时间": heart.index.to_series().shift(),
            "结束时间": heart.index,
            "间隔（分钟）": interval,
        }
    )
    gaps = gaps.loc[interval > 60]
    print("超过一小时的相邻记录间隔：\n" + gaps.to_string(index=False))
    print(f"长缺口共 {len(gaps)} 段；最长 {gaps['间隔（分钟）'].max():.0f} 分钟")

    description = heart.describe().rename(
        index={
            "count": "数量",
            "mean": "均值",
            "std": "标准差",
            "min": "最小值",
            "25%": "第一四分位数",
            "50%": "中位数",
            "75%": "第三四分位数",
            "max": "最大值",
        }
    )
    print("描述统计：\n" + description.round(3).to_string())
    q1, q3 = heart.quantile([0.25, 0.75])
    low, high = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
    outlier = (heart < low) | (heart > high)
    print(
        f"IQR 界限：{low:.1f}～{high:.1f} bpm；异常值 {outlier.sum()} 条，占 {outlier.mean():.3%}"
    )
    print(f"超出 30～220 bpm 的观测：{((heart < 30) | (heart > 220)).sum()} 条")


if __name__ == "__main__":
    run_step_two(load_heart_rate())
