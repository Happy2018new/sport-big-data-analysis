import numpy as np
from common import Config
from step_one_stationarity import run_step_one
from step_two_order import run_step_two
from step_three_diagnosis import run_step_three
from step_four_forecast import run_step_four

if __name__ == "__main__":
    np.random.seed(Config.SEED)
    train, test, adf = run_step_one()
    order, grid = run_step_two(train)
    model, coefficients, tests = run_step_three(train, order)
    predictions, metrics = run_step_four(train, test, model)
