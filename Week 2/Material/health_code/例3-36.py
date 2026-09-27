import pandas as pd
from pyecharts.charts import Pie,Bar,Grid
import pyecharts.options as opts
from pyecharts.globals import ThemeType
import webbrowser

df = pd.read_csv('../data/people.csv', index_col='年份')
df.drop('年末总人口(万人)',axis=1,inplace=True)

pie = (Pie()
    .add('',[list(z) for z in zip(df.columns.tolist(),df.loc['2022年'].tolist())],
         radius=(20,100),center=(600,300))
         # radius=(20,100),)
    .set_series_opts(label_opts=opts.LabelOpts(formatter='{b}:\n{c} {d}%'))
    .set_global_opts(title_opts=opts.TitleOpts(title='2022年全国各年龄段人口饼图',pos_left='60%'),
    # .set_global_opts(title_opts=opts.TitleOpts(title='2022年全国各年龄段人口饼图'),
                     legend_opts=opts.LegendOpts(is_show=False)))
bar = (Bar()
    .add_xaxis(df.columns.tolist())
    .add_yaxis('',df.loc['2022年'].tolist())
    .set_global_opts(title_opts=opts.TitleOpts(title='2022年全国各年龄段人口柱状图'),
                    legend_opts=opts.LegendOpts(is_show=False)))
grid = (Grid(init_opts=opts.InitOpts(width="800px", height="500px",theme=ThemeType.VINTAGE))
    .add(bar,grid_opts=opts.GridOpts(pos_right='50%'))
    .add(pie,grid_opts=opts.GridOpts(pos_left='50%')))
grid.render(r'..\chart\例3-36.html')
webbrowser.open(r'..\chart\例3-36.html')