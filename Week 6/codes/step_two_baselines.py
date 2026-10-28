import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from common import Config, evaluate, split_data


def run_step_two() -> pd.DataFrame:
    """建立基线模型"""
    print("=" * 25)
    x_train, x_test, y_train, y_test = split_data()
    recent = LinearRegression().fit(x_train[["Test_11"]], y_train)
    rows = [
        [
            "均值基线",
            0,
            *evaluate(y_train, np.full(len(y_train), y_train.mean())),
            *evaluate(y_test, np.full(len(y_test), y_train.mean())),
        ],
        [
            "Test_11回归",
            1,
            *evaluate(y_train, recent.predict(x_train[["Test_11"]])),
            *evaluate(y_test, recent.predict(x_test[["Test_11"]])),
        ],
    ]
    print(f"训练/测试人数: {len(y_train)}/{len(y_test)}, 随机种子: {Config.SEED}")
    print(f"训练/测试均值: {y_train.mean():.4f}/{y_test.mean():.4f}分")
    print(f"测试总体标准差: {y_test.std(ddof=0):.4f}分")
    return pd.DataFrame(rows, columns=Config.METRIC_COLUMNS)
