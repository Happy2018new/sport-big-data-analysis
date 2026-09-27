import webbrowser

import pandas as pd
from pyecharts.charts import Line, Bar
import pyecharts.options as opts

df = pd.read_excel(r'..\data\2016-2022年全国卫生医疗情况简表.xls')
df['年份'] = df['年份'].astype(str)
# 条形图+折线图
bar = (Bar()
       .add_xaxis(df['年份'].tolist())
       .add_yaxis('人均住院费用（元）', df['人均住院费用（元）'].tolist(),
                  bar_width=20, label_opts=opts.LabelOpts(is_show=False),
                  yaxis_index=0)
       .set_global_opts(title_opts=opts.TitleOpts(title='2016-2022年医院入院人数及住院费用数据图'),
                        xaxis_opts=opts.AxisOpts(name='年份',
                                                 name_location='center',name_gap=20),
                        yaxis_opts=opts.AxisOpts(name='人均住院费用（元）',
                                                 name_location='center',
                                                 name_gap=50, min_=0, max_=15000),
                        legend_opts=opts.LegendOpts(pos_top='bottom'),
                        toolbox_opts=opts.ToolboxOpts(is_show=True),
                        tooltip_opts=opts.TooltipOpts(trigger='item'))
       .extend_axis(yaxis=opts.AxisOpts(name='入院人数（万人）', name_location='center',
                                        type_="value", position="right",name_gap=50)))

line = (Line().add_xaxis(df['年份'].tolist())
        .add_yaxis('入院人数（万人）', df['入院人数（万人）'].tolist(), yaxis_index=1))

bar.overlap(line)
bar.render(r'..\chart\例3-35.html')
webbrowser.open(r'..\chart\例3-35.html')