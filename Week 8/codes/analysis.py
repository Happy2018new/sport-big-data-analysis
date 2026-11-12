from step_one_prepare import run_step_one
from step_two_clustering import run_step_two
from plot import plot_original, plot_selection, plot_clusters


def main() -> None:
    """读取数据、完成聚类并输出三张SVG。"""
    data = run_step_one()
    plot_original(data)
    result, quality, centers = run_step_two(data)
    plot_selection(quality)
    plot_clusters(result, centers)


if __name__ == "__main__":
    main()
