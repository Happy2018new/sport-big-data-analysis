import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/大众健身运动项目参与度.csv',
                 encoding='utf-8')

plt.rcParams['font.sans-serif'] = 'SimHei'

facetGrid = sns.catplot(data=df, x='运动方式', y='比例',
                        height=4, aspect=2, width=0.8,
                        kind='bar')
# facetGrid = sns.barplot(data=df,x='运动方式',y='比例',
#                         width=0.5)
for i, v in enumerate(df['比例']):
    facetGrid.ax.text(i, v, str(v) + "%", ha='center',
                   va='bottom')
    # facetGrid.ax.text(i, v, str(v)+"%", ha='center', va='bottom')
    # facetGrid.ax.text(i, v, '%s'%v+"%", ha='center', va='bottom')
    # facetGrid.ax.text(i, v, '{}'.format(v)+"%", ha='center', va='bottom')
    # facetGrid.ax.text(i, v, f'{v}'+"%", ha='center', va='bottom')

plt.xticks(df['运动方式'],rotation=45)
plt.title('大众健身运动项目参与度')
plt.tight_layout()
plt.show()
