import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Week 2/Material/data/heartRate.csv", encoding="utf-8")
df["datetime"] = pd.to_datetime(df["datetime"])

# 按日期分组
startDate = ["2023-6-2", "2023-6-3", "2023-6-4"]
endDate = ["2023-6-3", "2023-6-4", "2023-6-5"]
heartRate = []
for i in range(3):
    select_df = df[(df["datetime"] >= startDate[i]) & (df["datetime"] < endDate[i])]
    heartRate.append(select_df["heartRate"].tolist())
# 绘制箱线图
plt.rcParams["font.sans-serif"] = "SimHei"
plt.boxplot(x=heartRate, labels=startDate)
plt.xlabel("日期", font="FangSong")
plt.ylabel("心率")
plt.title("某同学某几日心率箱线图")
plt.show()
