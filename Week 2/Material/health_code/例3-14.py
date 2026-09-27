import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../data/heartRate.csv', encoding='utf-8')
df['datetime'] = pd.to_datetime(df['datetime'])
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.figure(figsize=(8, 5))
plt.plot(df['datetime'], df['heartRate'], marker='o', label='心率')

plt.legend()
plt.xlabel('时间')
plt.ylabel('心率')
plt.xlim((pd.to_datetime('2023-6-2 06:0:0'), pd.to_datetime('2023-6-2 09:0:0')))
plt.title('某同学2023年6月1日-6月5日某时间段心率')
plt.show()
