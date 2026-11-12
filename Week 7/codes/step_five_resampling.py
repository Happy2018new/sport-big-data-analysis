import pandas as pd
from common import Config, load_heart_rate
from plot import plot_resampling


def run_step_five(day: pd.Series) -> None:
    """比较十分钟聚合及缺失值处理，不扩展原始记录的边界。"""
    aggregation = day.resample("10min").agg(["mean", "median", "max", "std"])
    mean = aggregation["mean"]
    strategies = pd.DataFrame(
        {
            "保留缺失值": mean,
            "线性插值": mean.interpolate(method="linear", limit_area="inside"),
            "前向填充": mean.ffill(),
        }
    )
    print("\n五、十分钟重采样")
    print(
        f"窗口总数：{len(mean)}；空窗：{mean.isna().sum()}；每窗最少观测：{day.resample('10min').count().min()}"
    )
    summary = aggregation.agg(["count", "mean", "std", "min", "max"]).T
    summary.columns = ["有效窗口", "均值", "标准差", "最小值", "最大值"]
    print("聚合结果统计：\n" + summary.round(3).to_string())
    comparison = strategies.agg(["count", "mean", "std", "min", "max"]).T
    comparison.columns = summary.columns
    print("缺失策略比较：\n" + comparison.round(3).to_string())
    print("上述窗口均有数据，因此三种策略结果一致；19:25 后的未观测时段不作外推。")
    plot_resampling(day, aggregation, strategies, Config.FIGURES)


if __name__ == "__main__":
    run_step_five(load_heart_rate().loc[Config.DAY])
