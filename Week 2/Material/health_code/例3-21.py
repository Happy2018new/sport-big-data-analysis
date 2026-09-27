import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/heartRate.csv', encoding='utf-8')
df['datetime'] = pd.to_datetime(df['datetime'])
startDate = '2023-6-2'
endDate = '2023-6-3'
select_df = df[(df['datetime'] >= startDate) & (df['datetime'] < endDate)]

plt.rcParams['font.sans-serif'] = 'SimHei'

sns.displot(data=select_df, x='heartRate', bins=15,kde=True)

plt.title('某学生某日心率直方图')
plt.tight_layout()
plt.show()
