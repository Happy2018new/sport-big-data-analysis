import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Week 2/Material/data/people.csv")

plt.rcParams["font.sans-serif"] = "SimHei"
plt.figure(figsize=(8, 5), dpi=300)
plt.scatter(df["年份"], df["0-14岁人口(万人)"], marker="o", color="r", label="0-14岁")
plt.scatter(df["年份"], df["15-64岁人口(万人)"], marker="s", c="blue", label="15-64岁")
plt.scatter(
    df["年份"], df["65岁及以上人口(万人)"], marker="*", c="green", label="65岁及以上"
)
plt.xlabel("年份")
plt.ylabel("年末总人口（万人）")
plt.legend()
# plt.ylim((8000,22000))
plt.xticks(df["年份"], rotation=45)
plt.title("2000-2022年年末各年龄段人口散点图")
plt.tight_layout()
plt.show()
