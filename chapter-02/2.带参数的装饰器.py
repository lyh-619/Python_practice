"""场景：调用一个不稳定的网络接口 fetch_data()，偶尔会抛异常。你希望失败后自动重试 N 次，每次间隔 delay 秒。"""
import functools
import time


# 要求：
# 实现 @retry(times=3, delay=0.5) 这样的带参数装饰器。
# 成功则正常返回；times 次都失败则抛出最后一次异常。
# 每次重试时打印日志，例如 第 2 次重试...。

# 提示：
# 带参数装饰器是"三层结构"：retry(times, delay) → 返回 decorator(func) → 返回 wrapper(*args, **kwargs)。
# 捕获异常用 try/except，记录最后一次异常用变量保存。
# 可以用 time.sleep 模拟延时（测试时把 delay 设小）。
# 加分项：用 raise last_exc from None 或保留原始 traceback。

def retry(times,delay):
    # times 表示总次数，失败后最多尝试 time -1 次
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            last_exc = None
            for t in range(1,times + 1):
                try:
                    return func(*args,**kwargs)
                except Exception as e:
                    last_exc = e
                    if t < times:
                        print(f'这是第{t}次失败，你还有{times-t}次机会，请{delay}秒后重试')
                        time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator

@retry(times=3,delay=0.5)
def fetch_data():
    pass
