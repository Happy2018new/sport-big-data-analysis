import pandas as pd
from sklearn.linear_model import LinearRegression
from common import Config, evaluate, split_data


def run_step_five(report: pd.DataFrame) -> pd.DataFrame:
    """模型改进"""
    print("=" * 25)

    x_train, x_test, y_train, y_test = split_data()
    selected = x_train.corrwith(y_train).abs().nlargest(3).index.tolist()
    model = LinearRegression().fit(x_train[selected], y_train)
    row = [
        "三个特征回归",
        len(selected),
        *evaluate(y_train, model.predict(x_train[selected])),
        *evaluate(y_test, model.predict(x_test[selected])),
    ]
    report = pd.concat(
        [report, pd.DataFrame([row], columns=Config.METRIC_COLUMNS)], ignore_index=True
    )

    print(f"选取特征: {'、'.join(selected)}")
    print("模型汇总: \n" + report.round(4).to_string(index=False))

    return report
