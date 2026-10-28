import pandas as pd
from step_one_exploration import run_step_one
from step_two_baselines import run_step_two
from step_three_regression import run_step_three
from step_four_diagnostics import run_step_four
from step_five_improvement import run_step_five


def run_experiment() -> None:
    """运行全部"""
    run_step_one()
    baselines = run_step_two()
    _, regression = run_step_three()
    run_step_four()
    report = pd.concat([baselines, regression], ignore_index=True)
    run_step_five(report)


run_experiment()
