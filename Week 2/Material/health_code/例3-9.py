import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Week 2/Material/data/heartRate.csv", encoding="utf-8")
df["datetime"] = pd.to_datetime(df["datetime"])

startDate = "2023-6-2"
endDate = "2023-6-3"
select_df = df[(df["datetime"] >= startDate) & (df["datetime"] < endDate)]

plt.rcParams["font.sans-serif"] = "SimHei"
plt.figure(figsize=(7, 4), dpi=300)
plt.hist(
    select_df["heartRate"],
    bins=10,
    range=(40, 200),
    density=False,
    color="skyblue",
    edgecolor="black",
    alpha=0.7,
)
plt.xlabel("心率区间")
plt.ylabel("频度")
plt.title("某学生某日心率直方图")
plt.show()
