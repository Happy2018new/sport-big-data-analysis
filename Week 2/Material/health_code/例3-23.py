import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/heartRate.csv', encoding='utf-8')
df['date'] = pd.to_datetime(df['datetime']).dt.date
plt.rcParams['font.sans-serif'] = 'SimHei'
sns.displot(data=df, x='heartRate', hue='date', kind='kde')
plt.title('某学生心率核密度图（分日期）')
plt.tight_layout()
plt.show()
