import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMAResultsWrapper
from plot import plot_forecast, plot_rolling


def run_step_four(
    train: pd.Series, test: pd.Series, model: ARIMAResultsWrapper
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """比较全年预测和逐日预测，逐日更新状态但不重新估计参数"""
    forecast = model.get_forecast(steps=len(test))
    predictions = pd.DataFrame(index=test.index)
    predictions["ARIMA一次预测"] = forecast.predicted_mean
    predictions["Naive逐日预测"] = (
        pd.concat([train.tail(1), test]).shift(1).loc[test.index]
    )
    predictions["训练均值"] = train.mean()
    interval = pd.DataFrame(forecast.conf_int(), index=test.index)
    plot_forecast(train, test, predictions, interval)

    # 每次先预测，再接收当天真实值
    rolling = []
    current = model
    for actual in test:
        rolling.append(float(current.forecast(steps=1)[0]))
        current = current.extend([actual])
    predictions["ARIMA逐日预测"] = rolling
    predictions["Naive固定起点"] = train.iloc[-1]
    rows = []
    for name in predictions:
        errors = test - predictions[name]
        rows.append([name, np.sqrt((errors**2).mean()), errors.abs().mean()])
    metrics = pd.DataFrame(rows, columns=["方法", "RMSE", "MAE"])
    print("\n四、2020年预测误差\n" + metrics.round(4).to_string(index=False))
    plot_rolling(test, predictions["ARIMA逐日预测"], predictions["Naive逐日预测"])
    return predictions, metrics
