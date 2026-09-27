import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('../data/学生运动数据.csv', index_col=0)
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.figure(figsize=(4, 4), dpi=300)

sns.relplot(data=df, x='step', y='calories', col='date',
            hue='distance', size='heartRate', kind='scatter')
plt.suptitle('某学生运行心率散点图（分日期）')
plt.tight_layout()
plt.show()
