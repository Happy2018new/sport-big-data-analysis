import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel("Week 2/Material/data/2016-2022年全国卫生技术人员统计表（万人）.xls")
length = df.shape[0]  # 获取df行数
width = 1.0 / (df.shape[1] - 1)  # 通过df列数调整列宽度，观测变量间无间隔
m = np.arange(length)


plt.rcParams["font.sans-serif"] = "SimHei"
plt.figure(figsize=(10, 6), dpi=300)
# 绘图
for i in range(len(df.columns) - 1):  # 通过df列数，决定依据多少种样本类型，进行绘图
    plt.bar(m + width * i, df[df.columns[i + 1]], width=width, label=df.columns[i + 1])
    for x, y in zip(m + width * i, df[df.columns[i + 1]]):
        plt.text(x, y, "%.1f" % y, ha="center", va="bottom", rotation=45)

plt.xlabel("年份")
plt.ylabel("人数（万人）")
plt.xticks(m, labels=df[df.columns[0]])
plt.ylim(0, 1250)
plt.legend(loc="best")

plt.title("2016-2022年全国卫生技术人员人数统计柱状图")
plt.show()
