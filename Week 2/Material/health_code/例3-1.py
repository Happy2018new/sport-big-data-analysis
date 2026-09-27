import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "Week 2/Material/data/全国医疗卫生机构床位数2016-2022.csv", encoding="ANSI"
)
plt.rcParams["font.sans-serif"] = "SimHei"
plt.figure(figsize=(10, 5), dpi=300)

plt.plot(df["年份"], df["床位数（万张）"], marker="o", color="r", label="床位数")
plt.legend()
plt.grid(axis="y", color="g", alpha=0.5, linestyle="-.")
plt.xlabel("年份")
plt.ylabel("床位数(万张)")
plt.title("2016-2022年全国医疗卫生机构床位数")
plt.show()
