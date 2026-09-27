import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('../data/employee.csv')
plt.rcParams['font.sans-serif'] = 'SimHei'
# 使用pairplot函数绘制散点图、直方图
sns.pairplot(data=df)
plt.show()