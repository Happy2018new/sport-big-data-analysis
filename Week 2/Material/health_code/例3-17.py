import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel(r'..\data\2016-2022年全国卫生医疗情况简表.xls')
plt.rcParams['font.sans-serif'] = 'SimHei'
# plt.figure(figsize=(7,7),dpi=300)

# sns.lineplot(x='年份', y='人口（万人）',
#              color='r', data=df)
sns.relplot(x='年份', y='人口（万人）',
            color='r', kind='line', data=df)
plt.title('2016-2022年全国人口变化折线图')
plt.tight_layout()
plt.show()
