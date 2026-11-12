import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from common import Config


def run_step_two(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """标准化两个指标，比较不同簇数后完成聚类。"""
    scaler = StandardScaler()
    x = scaler.fit_transform(data[Config.FEATURES])
    scores = []
    for k in range(2, 6):
        model = KMeans(
            n_clusters=k, init="k-means++", n_init=10, random_state=Config.SEED
        ).fit(x)
        scores.append([k, model.inertia_, silhouette_score(x, model.labels_)])
    quality = pd.DataFrame(scores, columns=["k", "sse", "silhouette"])
    best_k = int(quality.loc[quality["silhouette"].idxmax(), "k"])
    model = KMeans(
        n_clusters=best_k, init="k-means++", n_init=10, random_state=Config.SEED
    ).fit(x)

    # 恢复原始单位，并按中心步数从少到多给簇编号。
    centers = pd.DataFrame(
        scaler.inverse_transform(model.cluster_centers_), columns=Config.FEATURES
    )
    order = centers["steps"].sort_values().index
    mapping = {old: new + 1 for new, old in enumerate(order)}
    result = data.copy()
    result["cluster"] = pd.Series(model.labels_).map(mapping)
    centers = centers.loc[order].reset_index(drop=True)
    centers.index = range(1, best_k + 1)
    print(f"选定簇数：{best_k}；轮廓系数：{quality['silhouette'].max():.4f}")
    summary = result.groupby("cluster").agg(
        记录数=("bpm", "size"), 平均步数=("steps", "mean"), 平均心率=("bpm", "mean")
    )
    summary["记录占比（%）"] = summary["记录数"] / len(result) * 100
    summary.index.name = "簇"
    print("聚类结果：\n" + summary.round(2).to_string())
    return result, quality, centers
