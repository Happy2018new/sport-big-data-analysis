def func(x, y):
    sum = x + y
    average = (x + y) / 2
    min_number = min(x, y)
    max_number = max(x, y)
    return (sum, average, min_number, max_number)


def func2(x, y):
    sum = x + y
    return (sum,)


# 对返回值进行一一对应赋值
# sum, average, min_number, max_number = func(12, 5)
# print("sum=", sum)
# print("average=", average)
# print("min=", min_number)
# print("max=", max_number)

# 对返回值进行自动解包对应赋值1
# sum1, *rest = func(10, 20)
# print("sum1=", sum1)
# print("rest=", rest)
#
# # 对返回值进行自动解包对应赋值2
# sum1, *middle, max1 = func(10, 30)
# print("sum1=", sum1)
# print("middle=", middle)
# print("max1=", max1)
#
# # 对返回值（元组（内有唯一值）进行解包）
sum2 = func2(20, 50)
print(sum2)

