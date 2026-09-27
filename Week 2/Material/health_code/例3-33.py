import pandas as pd
from pyecharts.charts import Bar
import pyecharts.options as opts
from pyecharts.globals import ThemeType
import webbrowser

df = pd.read_excel(r'..\data\2016-2022年全国卫生技术人员统计表（万人）.xls')
# 条形图

bar = (
    Bar(init_opts=opts.InitOpts(width="800px", height="400px",
                                page_title="HHHHHH", theme=ThemeType.LIGHT))
    .add_xaxis(df['年份'].tolist())
    .add_yaxis('执业（助理）医师', df['执业（助理）医师'].tolist(), stack='1',
               label_opts=opts.LabelOpts(position='top'))
    .add_yaxis('注册护士', df['注册护士'].tolist(), stack='2')
    .add_yaxis('其他', df['其他'].tolist(), stack='3')
    .set_global_opts(title_opts=opts.TitleOpts(title='2016-2022年全国卫生技术人员条形图'),
                     xaxis_opts=opts.AxisOpts(name='年份'),
                     yaxis_opts=opts.AxisOpts(name='人(万人)'),
                     legend_opts=opts.LegendOpts(pos_top='top', pos_left='right'),
                     toolbox_opts=opts.ToolboxOpts(is_show=True, pos_top='bottom', pos_left='center'),
                     tooltip_opts=opts.TooltipOpts(trigger='item'),
                     )
)
bar.render(r'例3-33.html')
webbrowser.open(r'例3-33.html')
# bar.render_notebook()
