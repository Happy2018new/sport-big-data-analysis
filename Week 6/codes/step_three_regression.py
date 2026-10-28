import pandas as pd
from plot import plot_predictions
from common import Config, evaluate, split_data
from sklearn.linear_model import LinearRegression


def run_step_three() -> tuple[LinearRegression, pd.DataFrame]:
    """多元线性回归建模"""
    x_train, x_test, y_train, y_test = split_data()
    model = LinearRegression().fit(x_train, y_train)
    train_prediction = model.predict(x_train)
    test_prediction = model.predict(x_test)
    row = [
        "全部特征回归",
        len(Config.FEATURES),
        *evaluate(y_train, train_prediction),
        *evaluate(y_test, test_prediction),
    ]
    plot_predictions(
        y_train,
        y_test,
        train_prediction,
        test_prediction,
        Config.FIGURES / "预测成绩与真实成绩.svg",
    )
    return model, pd.DataFrame([row], columns=Config.METRIC_COLUMNS)
