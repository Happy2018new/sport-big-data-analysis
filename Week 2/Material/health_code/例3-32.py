import pandas as pd
from pyecharts.charts import Scatter
import pyecharts.options as opts
import webbrowser
from pyecharts.globals import ThemeType

df = pd.read_csv('../data/people.csv')
df['年份'] = df['年份'].astype(str)

# 散点图
scatter = (
    Scatter(init_opts=opts.InitOpts(width="800px",
                                    height="400px",theme=ThemeType.SHINE))
    .add_xaxis(df['年份'].tolist())
    .add_yaxis('0-14岁人口(万人)', df['0-14岁人口(万人)'],
               label_opts=opts.LabelOpts(is_show=False))
    .add_yaxis('15-64岁人口(万人)', df['15-64岁人口(万人)'],
               label_opts=opts.LabelOpts(is_show=False))
    .add_yaxis('65岁及以上人口(万人)', df['65岁及以上人口(万人)'],
               label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title='2000-2022年年末各年龄段人口散点图'),
                     xaxis_opts=opts.AxisOpts(name='年份'),
                     yaxis_opts=opts.AxisOpts(name='人口(万人)'),
                     legend_opts=opts.LegendOpts(pos_top='bottom', pos_left='right'),
                     toolbox_opts=opts.ToolboxOpts(is_show=True,
                                                   pos_top='bottom', pos_left='left'),
                     tooltip_opts=opts.TooltipOpts(trigger='axis'))
)
scatter.render(r'..\chart\例3-32.html')
webbrowser.open(r'..\chart\例3-32.html')
# scatter.render_notebook()
