a = 12.567
print("a=", a)                           # 第1种：直接输出
print("---------------")

print("a={}".format(a))                  # 第2种：作为format的参数输出
print("a={:.2f}".format(a))              # 第2种的扩展：format+格式化输出
print("---------------")

print(f"a={a}")                          # 第3种：f输出
print(f"a={a:.2f}")                      # 第3种的扩展：f+格式化输出
print("---------------")

print("a=%f" % a)                        # 第4种：%输出
print("a=%.2f" % a)                      # 第4种的扩展：%+格式化输出
