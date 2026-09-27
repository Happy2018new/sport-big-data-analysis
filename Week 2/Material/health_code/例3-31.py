import pandas as pd
from pyecharts.charts import Line
import pyecharts.options as opts
import webbrowser

df = pd.read_excel(r'..\data\2016-2022年全国卫生医疗情况简表.xls')

df['年份'] = df['年份'].astype(str)

# 折线图
a = Line(init_opts=opts.InitOpts(width="800px", height="400px"))
a.add_xaxis(xaxis_data=df['年份'].tolist())
a.add_yaxis(series_name='卫生技术人员（万人）', y_axis=df['卫生技术人员（万人）'].tolist())
a.add_yaxis(series_name='医疗床位数（万张）', y_axis=df['医疗床位数（万张）'].tolist())
a.add_yaxis(series_name='入院人数（万人）', y_axis=df['入院人数（万人）'].tolist())
a.add_yaxis('诊疗人次数（亿）', df['诊疗人次数（亿）'].tolist())
a.set_global_opts(title_opts=opts.TitleOpts(title='2016-2022年全国卫生医疗情况数据图', pos_left='center'),
                 legend_opts=opts.LegendOpts(pos_top='bottom'),
                 toolbox_opts=opts.ToolboxOpts(is_show=True),
                 tooltip_opts=opts.TooltipOpts(trigger='axis'))
     # )
a.render(r'..\chart\例3-31.html')
webbrowser.open(r'..\chart\例3-31.html')
# a.render_notebook()
