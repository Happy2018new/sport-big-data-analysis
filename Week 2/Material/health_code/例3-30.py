import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel(r'..\data\2016-2022年全国卫生医疗情况简表.xls')
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

sns.residplot(data=df, x='年份',
              y='人均住院费用（元）', order=1)
plt.show()
