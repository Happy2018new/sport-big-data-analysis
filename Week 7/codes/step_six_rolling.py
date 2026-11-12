import pandas as pd
from common import Config, load_heart_rate
from plot import plot_rolling


def run_step_six(day: pd.Series) -> None:
    """比较三十分钟后向窗口与中心窗口，量化全局峰值时刻差。"""
    rolling = pd.DataFrame(
        {
            "后向平均": day.rolling("30min", min_periods=1).mean(),
            "中心平均": day.rolling("30min", center=True, min_periods=1).mean(),
        }
    )
    print("\n六、三十分钟滑动平均")
    print(f"原始峰值：{day.max():.3f} bpm，时刻 {day.idxmax():%H:%M}")
    for name in rolling.columns:
        series = rolling[name]
        delay = (series.idxmax() - day.idxmax()).total_seconds() / 60
        print(
            f"{name}：峰值 {series.max():.3f} bpm，时刻 {series.idxmax():%H:%M}，时刻差 {delay:.0f} 分钟；标准差 {series.std():.3f} bpm"
        )
    print("全局峰值时刻差受峰值削弱和峰形改变影响，不能当作固定相位延迟。")
    plot_rolling(day, rolling, Config.FIGURES)


if __name__ == "__main__":
    run_step_six(load_heart_rate().loc[Config.DAY])
