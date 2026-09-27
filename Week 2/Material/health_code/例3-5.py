import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../data/people.csv')

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.figure(figsize=(8, 10),dpi=300)
plt.scatter(df['年份'], df['65岁及以上人口(万人)'], marker='*', c='green', label='65岁及以上')
plt.xlabel('年份')
plt.ylabel('年末总人口（万人）')
plt.legend()
plt.xticks(df['年份'], rotation=45)
plt.title('2000-2022年65岁及以上人口散点图')
plt.tight_layout()
plt.show()
