import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/heartRate.csv', encoding='utf-8')
df['datetime'] = pd.to_datetime(df['datetime'])
df['date'] = df['datetime'].dt.date

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.figure(figsize=(12, 6), dpi=300)
plt.subplot(1, 2, 1)
sns.boxplot(data=df, x='date', y='heartRate',
            hue='date', legend=False)

plt.subplot(1, 2, 2)
sns.boxenplot(data=df, x='date', y='heartRate',
              hue='date', legend=False)
plt.tight_layout()
plt.show()
