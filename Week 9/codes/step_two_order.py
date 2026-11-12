import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf
from plot import plot_correlations


def run_step_two(train: pd.Series) -> tuple[tuple[int, int, int], pd.DataFrame]:
    """确定差分阶数后, 比较十六组 (p,q) 取值的 AIC 和 BIC 指标"""
    difference = train.diff().dropna()
    print(f"\n二、定阶：一次差分的ACF(1)={acf(difference, nlags=1)[1]:.6f}")
    rows = []
    for p in range(4):
        for q in range(4):
            model = ARIMA(train.to_numpy(), order=(p, 1, q), trend="n").fit()
            rows.append([p, q, model.aic, model.bic, model.mle_retvals["converged"]])
    grid = pd.DataFrame(rows, columns=["p", "q", "AIC", "BIC", "收敛"])
    valid = grid.loc[grid["收敛"]]
    best = valid.loc[valid["AIC"].idxmin()]
    order = (int(best["p"]), 1, int(best["q"]))
    print(grid.round(3).to_string(index=False))
    print(f"按AIC选择ARIMA{order}，模型不包含漂移项。")
    plot_correlations(difference)
    return order, grid
