import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/heartRate.csv', encoding='utf-8')
df['datetime'] = pd.to_datetime(df['datetime'])
df['date'] = df['datetime'].dt.date

plt.rcParams['font.sans-serif']='SimHei'
sns.catplot(data=df,x='date',y='heartRate',
            hue='date',kind='box')
plt.show()