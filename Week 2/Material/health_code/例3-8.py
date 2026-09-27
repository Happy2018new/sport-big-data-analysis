import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel(
    r"Week 2/Material/data/2016-2022年全国卫生技术人员统计表（万人）.xls"
)

length = df.shape[0]  # 获取df行数
m = np.arange(length)
# m = list(range(length))

plt.rcParams["font.sans-serif"] = " SimHei"
plt.figure(figsize=(10, 7), dpi=300)
# 绘图
bottom = 0
for i in range(1, len(df.columns) - 1):
    plt.bar(m, df[df.columns[i + 1]], bottom=bottom, label=df.columns[i + 1])
    bottom = bottom + df[df.columns[i + 1]]
    for x, y in zip(m, bottom):
        # plt.text(x, y, '%0.1f' % y, ha='center', va='bottom')
        plt.text(x, y, "{:.1f}".format(y), ha="center", va="bottom")
plt.xticks(ticks=m, labels=df[df.columns[0]])
plt.xlabel("年份")
plt.ylabel("人数（万人）")
plt.xticks(m, labels=df[df.columns[0]])

plt.legend(loc="best")

plt.title("2016-2022年全国卫生技术人员人数柱状图")
plt.show()
