import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel(r'..\data\2016-2022年全国卫生医疗情况简表.xls')
plt.rcParams['font.sans-serif'] = 'SimHei'
fig = plt.figure(figsize=(8, 5),dpi=300)
ax1 = fig.add_subplot()
# 添加双轴
ax2 = ax1.twinx()
# 绘制折线图
p1, = ax1.plot(df['年份'], df['医疗床位数（万张）'],
               marker='o', color='r', label='医疗床位数（万张）')
p2, = ax2.plot(df['年份'], df['入院人数（万人）'],
               marker='o', color='g', label='入院人数（万人）')
# 设置Y轴范围
ax1.set(ylim=(600, 1000), xlabel="年份", ylabel="医疗床位数（万张）")
ax2.set(ylim=(20000, 30000), ylabel="入院人数（万人）")
# 设置图例
plt.legend(handles=[p1, p2], loc='upper left')
# 设置Y轴label颜色与折线颜色相同
ax1.yaxis.label.set_color(p1.get_color())
ax2.yaxis.label.set_color(p2.get_color())
# 设置Y轴line颜色与折线颜色相同
ax2.spines.left.set_color(p1.get_color())
ax2.spines.right.set_color(p2.get_color())
# 设置Y轴ticks颜色与折线颜色相同
ax1.tick_params(axis='y', colors=p1.get_color())
ax2.tick_params(axis='y', colors=p2.get_color())

plt.title('2016-2022年全国医疗床位与入院人数情况折线图')
plt.show()
