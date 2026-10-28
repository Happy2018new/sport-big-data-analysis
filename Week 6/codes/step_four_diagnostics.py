import pandas as pd
import statsmodels.api as sm
from plot import plot_residuals
from common import Config, split_data
from statsmodels.stats.outliers_influence import variance_inflation_factor


def run_step_four() -> pd.DataFrame:
    """回归诊断与深入解读"""
    print("=" * 25)

    x_train, x_test, y_train, y_test = split_data()
    design = sm.add_constant(x_train)
    model = sm.OLS(y_train, design).fit()
    table = pd.DataFrame(
        {
            "回归系数": model.params.drop("const"),
            "VIF": [
                variance_inflation_factor(design.values, index)
                for index in range(1, design.shape[1])
            ],
            "与目标的训练集相关系数": x_train.corrwith(y_train),
        }
    )

    print(f"多元回归截距: {model.params['const']:.4f}")
    print("系数与共线性诊断: \n" + table.round(4).to_string())

    plot_residuals(
        y_train,
        y_test,
        model.fittedvalues.to_numpy(),
        model.predict(sm.add_constant(x_test)).to_numpy(),
        Config.FIGURES / "回归残差诊断.svg",
    )
    return table
