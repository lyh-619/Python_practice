"""题目背景
你需要一个「无限」的斐波那契数列来源，
但绝不能一次性生成所有值（内存有限）。
同时要在此基础上做一个「只取前 N 个偶数项」的过滤流水线。
"""
from itertools import count


# 目标
# 用生成器函数实现两个环节：环节 A 无限产出斐波那契数；
# 环节 B 接收环节 A，惰性过滤出偶数并只取前 N 个。
# 要求整个链条在你主动请求之前不产生任何计算（可通过在生成器内打印观察求值时机）。

# 环节A：无限生成斐波那契数列
def fibo_a():
    print('【环节A】生成器启动')
    a,b = 1,1
    while True:
        yield a
        a,b = b,a+b

# 环节B：惰性过滤流水线
def fibo_b(n):
    print(f'【环节B】过滤器启动，取{n}个偶数')
    if n<=0:
        return
    count = 0
    for x in fibo_a():
        if x % 2 == 0:
            count+=1
            print(f'这是第{count}个偶数：{x}')
            yield x
            if count>=n:
                print('已达到目标数量')
                return

# 测试
for num in fibo_b(5):
    print(num)