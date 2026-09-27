import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('../data/学生运动数据.csv')
plt.rcParams['font.sans-serif'] = 'SimHei'

plt.subplot(1, 2, 1)
# 分类散点图
sns.stripplot(data=df, x='date', y='heartRate', hue='step')

plt.subplot(1, 2, 2)
# 分簇散点图（蜂群图）
sns.swarmplot(data=df, x='date', y='heartRate', hue='step')
plt.tight_layout()
plt.show()
