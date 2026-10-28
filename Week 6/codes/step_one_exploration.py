from common import Config, load_data
from plot import plot_correlation


def run_step_one() -> None:
    """数据探索"""
    print("=" * 25)

    df = load_data()
    scores = df.drop(columns="Student_ID")
    description = scores.describe().T[["mean", "std", "min", "max"]]
    description.columns = ["平均数", "标准差", "最小值", "最大值"]

    print(f"数据形状 (行数, 列数): {df.shape}")
    print("-" * 5)
    print("前五行: \n" + df.head().to_string(index=False))
    print("-" * 5)
    print("描述统计: \n" + description.round(2).to_string())
    print("-" * 5)
    print(f"缺失值: {df.isna().sum().sum()}")
    print(f"越界成绩: {((scores < 0) | (scores > 100)).sum().sum()}")

    correlation = scores.corr()
    plot_correlation(correlation, Config.FIGURES / "成绩相关系数热力图.svg")
    target_correlation = correlation.loc[Config.FEATURES, Config.TARGET]
    best = target_correlation.idxmax()
    print(
        f"T1: 与 Test_12 相关性最高的是 {best}, 相关系数为 {target_correlation[best]:.4f}"
    )
