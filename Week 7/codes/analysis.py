from step_one_prepare import run_step_one
from step_two_quality import run_step_two
from step_three_visualization import run_step_three
from step_four_daily import run_step_four
from step_five_resampling import run_step_five
from step_six_rolling import run_step_six


def run_experiment() -> None:
    """按作业顺序完成解析、质量检查和可视化。"""
    heart = run_step_one()
    run_step_two(heart)
    run_step_three(heart)
    day = run_step_four(heart)
    run_step_five(day)
    run_step_six(day)
    print("\n已完成实验，SVG 图片保存在 Week 7/figures 中。")


if __name__ == "__main__":
    run_experiment()
