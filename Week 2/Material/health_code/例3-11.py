import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Week 2/Material/data/heartRate.csv", encoding="utf-8")
df["datetime"] = pd.to_datetime(df["datetime"])
# 按日期分组
grouped = df.groupby(df["datetime"].dt.date)
# 绘制箱线图
plt.rcParams["font.sans-serif"] = "SimHei"
plt.figure(figsize=(8, 5), dpi=300)
plt.boxplot(
    x=[y["heartRate"] for _, y in grouped],
    labels=[str(x) for x, _ in grouped],
    notch=True,
    vert=True,
    meanline=False,
    showmeans=True,
)
# plt.xlabel('日期', font='FangSong', fontsize=20)
plt.xlabel("日期")
plt.ylabel("心率")
plt.title("某同学某几日心率箱线图")
plt.show()
