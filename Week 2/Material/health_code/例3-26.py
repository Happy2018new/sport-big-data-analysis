import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('../data/学生运动数据.csv')
plt.rcParams['font.sans-serif'] = 'SimHei'

# sns.stripplot(data=df,x='date',y='heartRate',hue='calories')
# sns.swarmplot(data=df,x='date',y='heartRate',hue='calories')
sns.catplot(data=df,x='date',y='heartRate',
            hue='heartRate',kind='swarm')
plt.show()