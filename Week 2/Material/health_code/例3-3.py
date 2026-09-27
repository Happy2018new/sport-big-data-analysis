import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = "SimHei"

df = pd.read_csv("Week 2/Material/data/heartRate.csv", encoding="utf-8")
df["datetime"] = pd.to_datetime(df["datetime"])
select_df = df[::10]  # 心率数据过于密集，进行切片处理

plt.figure(figsize=(12, 5))
plt.plot(select_df["datetime"], select_df["heartRate"], marker="o", label="心率")
plt.legend()
plt.xlabel("日期")
plt.ylabel("心率")
plt.title("某学生2023年6月1日-6月5日心率")
plt.show()
