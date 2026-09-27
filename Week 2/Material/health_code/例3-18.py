import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('../data/学生运动数据.csv')
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.figure(figsize=(7, 4), dpi=300)

sns.scatterplot(x='step', y='calories',
                hue='distance', size='heartRate', data=df)
# sns.relplot(x='step',y='heartRate',
#             hue='distance',size='calories',data=df)
plt.title('某学生运动相关数据散点图(不分日期)')
plt.tight_layout()
plt.show()
