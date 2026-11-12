import pandas as pd
from statsmodels.tsa.arima.model import ARIMA, ARIMAResultsWrapper
from statsmodels.stats.diagnostic import acorr_ljungbox
from plot import plot_residuals


def run_step_three(
    train: pd.Series, order: tuple[int, int, int]
) -> tuple[ARIMAResultsWrapper, pd.DataFrame, pd.DataFrame]:
    """拟合模型"""
    model = ARIMA(train.to_numpy(), order=order, trend="n").fit()
    coefficients = pd.DataFrame(
        {"coef": model.params, "std err": model.bse, "P>|z|": model.pvalues},
        index=model.param_names,
    )
    burn = model.loglikelihood_burn
    residuals = pd.Series(model.resid[burn:], index=train.index[burn:])
    p, _, q = order
    tests = acorr_ljungbox(residuals, lags=[10, 20, 30], model_df=p + q)
    print("\n三、模型系数\n" + coefficients.to_string(float_format="%.6g"))
    print(
        "残差Ljung–Box检验（已扣除AR、MA参数的自由度）：\n" + tests.round(6).to_string()
    )
    plot_residuals(residuals)
    return model, coefficients, tests
