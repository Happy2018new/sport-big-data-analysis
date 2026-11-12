import pandas as pd
from common import Config, load_heart_rate
from plot import plot_daily


def run_step_four(heart: pd.Series) -> pd.Series:
    """截取指定日期，输出有效时段和极值时刻。"""
    day = heart.loc[Config.DAY]
    print("\n四、单日心率")
    print(f"日期：{Config.DAY}；有效记录：{len(day)} 条")
    print(f"覆盖时段：{day.index.min():%H:%M}～{day.index.max():%H:%M}")
    print(f"均值：{day.mean():.3f} bpm；标准差：{day.std():.3f} bpm")
    for name, value in [("最小值", day.min()), ("最大值", day.max())]:
        times = day.index[day == value].strftime("%H:%M").tolist()
        print(f"{name}：{value} bpm；出现时刻：{'、'.join(times)}")
    plot_daily(day, Config.FIGURES)
    return day


if __name__ == "__main__":
    run_step_four(load_heart_rate())
