import pandas as pd
from pyecharts.charts import Timeline, Line
import pyecharts.options as opts
import webbrowser

df = pd.read_csv('../data/gupiao.csv', encoding='utf-8')
selected_df = df[['type', 'date', 'zhishu']]
selected_df['date'] = pd.to_datetime(selected_df['date']).dt.date
selected_df = selected_df.sort_values('date')
wide_df = selected_df.pivot(index='type', columns='date')
wide_df.columns = wide_df.columns.droplevel(0)

timeline = Timeline()
for i in range(2, len(wide_df.columns) + 1):
    # 标注日期用
    start_date = str(wide_df.columns[1])
    end_date = str(wide_df.columns[i - 1])

    x_data = wide_df.columns[1:i]
    y1_data = wide_df.iloc[0, 1:i]
    y2_data = wide_df.iloc[1, 1:i]
    y3_data = wide_df.iloc[2, 1:i]
    line = (Line())
    line.add_xaxis(x_data.tolist())
    line.add_yaxis('上证指数', y1_data.tolist(), is_smooth=True, is_symbol_show=False,
                   linestyle_opts=opts.LineStyleOpts(width=2),
                   markpoint_opts=opts.MarkPointOpts(
                       data=[
                           opts.MarkPointItem(name=start_date, coord=[0, y1_data[0]], value=y1_data[0], symbol_size=8),
                           opts.MarkPointItem(name=end_date, coord=[len(x_data) - 1, y1_data[-1]], value=y1_data[-1],
                                              symbol_size=8),
                       ],
                       symbol='circle',
                       label_opts=opts.LabelOpts(color='black')
                   )
                   )
    line.add_yaxis('沪深300指数', y2_data.tolist(), is_smooth=True, is_symbol_show=False,
                   linestyle_opts=opts.LineStyleOpts(width=2),
                   markpoint_opts=opts.MarkPointOpts(
                       data=[
                           opts.MarkPointItem(name=start_date, coord=[0, y2_data[0]], value=y2_data[0], symbol_size=8),
                           opts.MarkPointItem(name=end_date, coord=[len(x_data) - 1, y2_data[-1]], value=y2_data[-1],
                                              symbol_size=8),
                       ],
                       symbol='circle',
                       label_opts=opts.LabelOpts(color='black')
                   )
                   )
    line.add_yaxis('深证指数', y3_data.tolist(), is_smooth=True, is_symbol_show=False,
                   linestyle_opts=opts.LineStyleOpts(width=2),
                   markpoint_opts=opts.MarkPointOpts(
                       data=[
                           opts.MarkPointItem(name=start_date, coord=[0, y3_data[0]], value=y3_data[0], symbol_size=8),
                           opts.MarkPointItem(name=end_date, coord=[len(x_data) - 1, y3_data[-1]], value=y3_data[-1],
                                              symbol_size=8),
                       ],
                       symbol='circle',
                       label_opts=opts.LabelOpts(color='black')
                   )
                   )
    line.set_global_opts(title_opts=opts.TitleOpts(title='中国股市指数曲线图'),
                         xaxis_opts=opts.AxisOpts(name='日期'),
                         yaxis_opts=opts.AxisOpts(name='指数值', axislabel_opts=opts.LabelOpts(color='red')),
                         )
    timeline.add(line, i)

timeline.add_schema(play_interval=500, is_auto_play=True, is_loop_play=False, is_timeline_show=False)
timeline.render('..\chart\例3-39.html')
webbrowser.open('..\chart\例3-39.html')
