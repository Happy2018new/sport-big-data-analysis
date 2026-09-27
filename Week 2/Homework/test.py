import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("employee.csv", encoding="utf-8")
df = df[10:20]

plt.rcParams["font.sans-serif"] = "SimHei"
plt.figure(figsize=(8, 5))

plt.plot(
    df["指标"],
    df["第一产业就业人员(万人)"],
    marker="o",
    color="r",
    label="第一产业就业人员",
)
plt.plot(
    df["指标"],
    df["第二产业就业人员(万人)"],
    marker="*",
    color="g",
    label="第二产业就业人员",
)
plt.plot(
    df["指标"],
    df["第三产业就业人员(万人)"],
    marker="s",
    color="b",
    label="第三产业就业人员",
)
plt.legend(loc="upper left")

plt.xlabel("年份")
plt.ylabel("人数（万人）")
plt.title("2010-2019年中国各产业人员变化折线图")
plt.show()
