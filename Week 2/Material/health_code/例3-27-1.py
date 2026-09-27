import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('../data/hr.csv', encoding='ansi')
df = df[df['部门'] == '销售部']
plt.rcParams['font.sans-serif'] = 'SimHei'

sns.catplot(data=df, x='离职', y='每月平均工作小时数（小时）',
            hue='满意度', kind='swarm')
# sns.swarmplot(data=df, x='离职', y='每月平均工作小时数（小时）',
#             hue='评分')
plt.xticks([0, 1], labels=['在职', '离职'])
# plt.xlabel("")
plt.title("某IT公司销售部人员工作时长分类散点图")
plt.tight_layout()
plt.show()
