import pandas as pd

df = pd.read_csv('../data/heartRate.csv', encoding='utf-8')
df['datetime'] = pd.to_datetime(df['datetime'])

# 按日期分组
grouped = df.groupby(df['datetime'].dt.date)
for x, y in grouped:
    print("x:", x)
    print("y:", y)
print("end")
