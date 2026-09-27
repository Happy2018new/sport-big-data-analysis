import pandas as pd

# 对于DataFrame
df = pd.DataFrame({
    'A': [1, 2, None],
    'B': [4, None, 6],
    'C': [50, 25, 0]
})

print(df)
print("-------------------")

# 默认情况下，pandas的mean函数会忽略缺失值
mean_value_df = df.mean()
print(mean_value_df)
print("-------------------")

# 干净数据，造成均值偏离(对于C列）
clean_df = df.dropna()
mean_value_clean_df = clean_df.mean()
print(mean_value_clean_df)

