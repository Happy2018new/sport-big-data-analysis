import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Week 2/Material/data/people.csv")

plt.rcParams["font.sans-serif"] = "SimHei"
plt.figure(figsize=(8, 5), dpi=300)
plt.bar(df["年份"], df["年末总人口(万人)"])
for a, b in zip(df["年份"], df["年末总人口(万人)"]):
    plt.text(
        a,
        b,
        "{}".format(b),
        ha="center",
        va="bottom",
        fontsize=7,
        rotation=45,
        c="green",
    )
plt.xlabel("年份")
plt.ylabel("年末总人口（万人）")
plt.xticks(df["年份"], rotation=45)
plt.ylim((120000, 145000))
plt.title("2000-2022年年末总人口条形图")
plt.tight_layout()
plt.show()
