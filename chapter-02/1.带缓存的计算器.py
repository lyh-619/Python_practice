"""场景：你写了一个递归计算斐波那契数列的函数 fib(n)，但 n=35 时明显很慢，因为重复计算太多。"""
import functools

# 要求：
# 自己写一个装饰器 @memoize，让函数自动缓存"相同参数"的计算结果。
# 装饰后 fib(35) 要能在瞬间返回。
# 打印缓存命中情况（比如 print(f"[cache hit] {args}")）。

# 提示：
# 装饰器本质是"接收函数，返回新函数"。
# 缓存字典放在装饰器外层，不要放在 wrapper 内部（否则每次调用都会重置）。
# 用 functools.wraps 保留原函数名。

# 思考：如果参数是列表（不可哈希）怎么办？先不考虑，做完后我们讨论。

def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args in cache:    # 第一步：判断 args 是否在 cache 里
            print(f'【cache hit】{args}')     # 命中打印 [cache hit] 日志
            return cache[args]      # return cache[args]
        else:                # 第二步：未命中 → 调 func 算结果
            result = func(*args)    # result = func(*args)
            cache[args] = result    # 第三步：存入cache cache[...] = result
            return result           # return result

    return wrapper

@memoize
def fib(n):
    if n < 2:
        return n
    else:
        return fib(n-1) + fib(n-2)

print(fib(15))
print(fib(35))


