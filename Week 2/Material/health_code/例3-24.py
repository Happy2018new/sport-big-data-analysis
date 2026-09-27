import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('../data/学生运动数据.csv')
plt.rcParams['font.sans-serif'] = 'SimHei'

# 使用pairplot函数绘制散点图、直方图
sns.pairplot(data=df,vars=['step','distance','calories'],
             kind='scatter')
plt.suptitle('某学生运动数据配对分布统计图')
plt.tight_layout()
plt.show()