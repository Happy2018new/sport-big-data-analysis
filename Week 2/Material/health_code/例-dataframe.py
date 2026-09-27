import pandas as pd

df = pd.read_excel('../data/2016-2022年全国卫生技术人员统计表（万人）.xls')
print(df)
# # print(df.shape)                       #得到数据集的长度与宽度
# #
# print(df.columns)                     #取数据集的所有列名
# print(df.columns[0])                  #取数据集的第一个列名
#
# #取数据集的列
# print(df[df.columns[0]])              #取第一列数据
# print(type(df[df.columns[0]]))
# print(df.iloc[:,0:1])                 #取第一列数据
# print(type(df.iloc[:,0:1]))
# print(df['年份'])                     #根据列名，取第一列数据

#取数据集的行
# print(df.iloc[1:3,:])                  #取第1、2行

#取数据集的行与列
# print(df.iloc[1:3]["卫生技术人员"])      #取"卫生技术人员"列的第1、2行
# print(df.iloc[-1, 1:2])                  # 取"卫生技术人员"列的最后一行
# print(type(df.iloc[-1, 1:2]))                  # 取"卫生技术人员"列的最后一行
# print(df.values[-1, 1:2])                # 取"卫生技术人员"列的最后一行
# print(type(df.values[-1, 1:2]))                # 取"卫生技术人员"列的最后一行

#组合条件，取数据集的部分
# print(df[df["卫生技术人员"] >= 1000])
# print(df[(df["卫生技术人员"] >= 1000) & (df["卫生技术人员"]<=1100)])
# print(type(df[(df["卫生技术人员"] >= 1000) & (df["卫生技术人员"]<=1100)]))
print(df[(df["卫生技术人员"] >= 1000) & (df["卫生技术人员"]<=1100)]["注册护士"])