import pandas as pd
from pyecharts.charts import Timeline, Line
import pyecharts.options as opts
import webbrowser

df = pd.read_csv('../data/heartRate.csv')
df['datetime'] = pd.to_datetime(df['datetime'])
df = df.sort_values('datetime')
df['date'] = df['datetime'].dt.date
print(set(df['date']))
date = sorted(list(set(df['date'])))
print(date)


timeline = Timeline()
for i in range(len(date)):
    line = (Line()
            .add_xaxis(df[df['date'] == date[i]]['datetime'].tolist())
            .add_yaxis('心率', df[df['date'] == date[i]]['heartRate'].tolist(), is_smooth=False)
            .set_global_opts(title_opts=opts.TitleOpts(title='某同学{}心率情况'.format(date[i]))))
    timeline.add(line, date[i])

timeline.add_schema(play_interval=2000, is_auto_play=True, is_timeline_show=False, symbol='arrow')
timeline.render(r'..\chart\例3-37.html')
# timeline.render_notebook()
webbrowser.open(r'..\chart\例3-37.html')
