import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("Week 2/Material/data/heartRate.csv", encoding="utf-8")
data = df["heartRate"]
plt.rcParams["font.sans-serif"] = "SimHei"
plt.figure(figsize=(6, 5), dpi=300)
box = plt.boxplot(data, labels=" ")
# 获取箱线图的相关统计数据
q1, median, q3 = np.percentile(data, [25, 50, 75])
whiskers = box["whiskers"]
lower_whisker = whiskers[0].get_ydata()[1]
upper_whisker = whiskers[1].get_ydata()[1]
# 标注四分位数和上下边缘的数据值
plt.text(1.1, q1, f"下四分位数（Q1）: {q1:.2f}")
plt.text(1.1, median, f"中位数: {median:.2f}")
plt.text(1.1, q3, f"上四分位数（Q3）: {q3:.2f}")
plt.text(1.1, lower_whisker, f"下边缘值: {lower_whisker:.2f}")
plt.text(1.1, upper_whisker, f"上边缘值: {upper_whisker:.2f}")
plt.xlabel("某几日数据")
plt.ylabel("心率")
plt.title("箱线图数据分布示例")
plt.show()
