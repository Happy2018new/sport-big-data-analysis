import pandas as pd
from statsmodels.tsa.stattools import adfuller
from common import load_close
from plot import plot_overview, plot_differences


def run_step_one() -> tuple[pd.Series, pd.Series, pd.DataFrame]:
    """划分训练与测试数据"""
    close = load_close()
    train, test = close.loc[:"2019"], close.loc["2020"]
    print(f"数据共{len(close)}条，训练集{len(train)}条，测试集{len(test)}条。")
    print(
        f"收盘价缺失{close.isna().sum()}条，重复日期{close.index.duplicated().sum()}条。"
    )
    rows = []
    series = [train, train.diff().dropna(), train.diff().diff().dropna()]
    for name, values in zip(["原序列", "一次差分", "二次差分"], series):
        statistic, p_value, lag, *_ = adfuller(values, regression="c", autolag="AIC")
        rows.append([name, statistic, p_value, lag])
    adf = pd.DataFrame(rows, columns=["序列", "ADF统计量", "p值", "滞后阶数"])
    print("\n一、训练集平稳性检验\n" + adf.round(6).to_string(index=False))
    plot_overview(close)
    plot_differences(train)
    return train, test, adf
