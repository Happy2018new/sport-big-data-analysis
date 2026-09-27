import pandas as pd
from pyecharts.charts import Pie
import pyecharts.options as opts
from pyecharts.globals import ThemeType
import webbrowser

df = pd.read_csv('../data/people.csv', index_col='年份')
df.drop('年末总人口(万人)',axis=1,inplace=True)

# print([list(z) for z in zip(df.columns.tolist(),df.loc['2022年'].tolist())])
# 饼图
pie= (
    Pie(init_opts=opts.InitOpts(width="700px", height="500px",theme=ThemeType.LIGHT))
    .add('',[list(z) for z in zip(df.columns.tolist(),df.loc['2022年'].tolist())])
    .set_series_opts(label_opts=opts.LabelOpts(formatter='{b}\n{c}({d}%) '))
    .set_global_opts(
        title_opts=opts.TitleOpts(title='2022年全国各年龄段人口统计饼图',pos_left='center'),
        legend_opts=opts.LegendOpts(pos_top='middle',pos_left='left',orient='vercital'),
        toolbox_opts=opts.ToolboxOpts(is_show=True,pos_top='bottom',pos_left='center'))
)
pie.render(r'..\chart\例3-34.html')
webbrowser.open(r'..\chart\例3-34.html')
# pie.render_notebook()
