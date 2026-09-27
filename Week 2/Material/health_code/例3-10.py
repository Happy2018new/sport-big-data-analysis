import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Week 2/Material/data/people.csv")
explode = [0, 0, 0.15]
labels = ["0-14岁", "15-64岁", "65岁及以上"]
# labels=df.columns[2:5]

plt.rcParams["font.sans-serif"] = "SimHei"
plt.figure(figsize=(7, 5), dpi=300)
plt.pie(
    x=df.iloc[-1, 2:5],
    explode=explode,
    labels=labels,
    autopct="%.1f%%",
    shadow=True,
    pctdistance=0.2,
    startangle=0,
)
plt.legend(loc="best")
plt.title("2022年全国各年龄段人口饼状图")
plt.tight_layout()
plt.show()
