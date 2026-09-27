import pandas as pd
from pyecharts.charts import Timeline, Bar
import pyecharts.options as opts
import webbrowser
from math_number import round_up_first_digit

# df = pd.read_csv('../data/GDP.csv', encoding='ANSI')
df = pd.read_csv('../data/GDP2.csv', encoding='ANSI')
df.fillna(0, inplace=True)
date = df.columns[1:65]

bar_width = 20

timeline = Timeline(init_opts=opts.InitOpts(page_title="世界各国GDP前十强（1960-2023年）", ))
for year in date:
    str_year = str(year)
    select_df = df[['Country', str_year]]
    sorted_df = select_df.sort_values(by=str_year, ascending=True).tail(10)
    # sorted_df = select_df.sort_values(by=str_year, ascending=False).head(10)
    sorted_df[str_year] = sorted_df[str_year] / 1e8
    sorted_df[str_year] = sorted_df[str_year].astype(int)
    # 设置x轴上限数据max_xaxis(xaxis_opts=opts.AxisOpts(name='美元（亿）',min_=0,max_=max_xaxis),)
    max_gdp_value = sorted_df[str_year].iloc[-1]
    # max_xaxis = max_gdp_value*1.5
    max_xaxis = round_up_first_digit(max_gdp_value)

    # 设置图片平移位置
    image_offset_x = [0] * 10
    scale = 0.05
    for i in range(len(sorted_df[str_year])):
        image_offset_x[i] = max_gdp_value / sorted_df[str_year].iloc[i] * 0.05 + 1

    # 设置柱子的颜色
    colors = []
    for country in sorted_df['Country']:
        if country == '中国':
            colors.append('red')
        else:
            colors.append(None)

    data_pair = []
    for k, v, c in zip(sorted_df['Country'], sorted_df[str_year], colors):
        data_pair.append(
            opts.BarItem(
                name=k,
                value=v,
                itemstyle_opts=opts.ItemStyleOpts(color=c)
            ))
    # 设置放置图片的数据
    markpoint_data = []
    for i in range(len(sorted_df['Country'])):
        country_image = "image://../image/" + sorted_df['Country'].iloc[i] + ".png"
        markpoint_data.append(
            opts.MarkPointItem(type_="image", name=sorted_df['Country'].iloc[i],
                               coord=[data_pair[i].opts['value'] * image_offset_x[i], sorted_df['Country'].iloc[i]],
                               symbol=country_image,
                               symbol_size=[bar_width * 1.5, bar_width],
                               ),
        )
    # 绘制柱状图
    bar = (Bar()
           .add_xaxis(sorted_df['Country'].tolist())
           .add_yaxis('国家', data_pair, stack=None, bar_width=bar_width)
           .set_series_opts(markpoint_opts=opts.MarkPointOpts(data=markpoint_data), )  # 放置图片
           .set_global_opts(title_opts=opts.TitleOpts(title='世界各国GDP前十强（1960-2023年）',
                                                      subtitle='数据来源：世界银行',
                                                      subtitle_link="https://www.shihang.org/zh/home",
                                                      pos_right='center'),

                            legend_opts=opts.LegendOpts(is_show=False),
                            xaxis_opts=opts.AxisOpts(name='美元（亿）', min_=0, max_=max_xaxis),
                            yaxis_opts=opts.AxisOpts(name='国家', axislabel_opts=opts.LabelOpts(color='red')),

                            graphic_opts=[opts.GraphicGroup(
                                graphic_item=opts.GraphicItem(left="80%", top="5%"),
                                children=[opts.GraphicText(
                                    graphic_textstyle_opts=opts.GraphicTextStyleOpts(text='年份：' + str_year,
                                                                                     font="14px Microsoft YaHei")
                                )]
                            )]
                            )
           .reversal_axis()
           )
    timeline.add(bar, str_year)

timeline.add_schema(play_interval=800, is_auto_play=True, is_loop_play=False, is_timeline_show=True)
timeline.render(r'..\chart\例3-38.html')
webbrowser.open(r'..\chart\例3-38.html')
