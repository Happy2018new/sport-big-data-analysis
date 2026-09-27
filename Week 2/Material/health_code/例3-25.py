import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('../data/学生运动数据.csv')
plt.rcParams['font.sans-serif'] = 'SimHei'

# 使用pairplot函数绘制散点图
sns.pairplot(data=df,x_vars=['distance','step'],
             y_vars=['calories','heartRate'],kind='kde')
plt.show()