import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.figure(figsize=(7,5),dpi=300)

# 画第1个图：折线图
x = np.arange(1, 100)
plt.subplot(2, 2, 1)
plt.plot(x, x * x)
plt.title('第1张子图')

# 画第2个图：散点图
plt.subplot(2, 2, 2)
plt.scatter(np.arange(0, 10), np.random.rand(10))
plt.title('第2张子图')

# 画第3个图：条形图
plt.subplot(2, 1, 2)
plt.bar([10, 20, 30, 40, 50], [25, 15, 35, 30, 20], color='b')
plt.title('第3张子图')

plt.suptitle('总图')
plt.tight_layout()
plt.show()
