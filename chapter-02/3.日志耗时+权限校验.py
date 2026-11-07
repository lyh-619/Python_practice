"""场景：Web 视图中既需要统计耗时，又需要校验用户登录。"""
import functools
import time


# 要求：
# @timer 打印 func 耗时 xx ms。
# @login_required 若无 user 参数则抛 PermissionError。
# 两个装饰器叠加，明确执行顺序。

def timer(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        start = time.perf_counter()
        try:
            return func(*args,**kwargs)
        finally:
            print(f'{func.__name__}耗时{(time.perf_counter()-start)*1000:.2f}ms')
    return wrapper

def login_required(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        if not kwargs.get('user'):
            raise PermissionError('未登录')
        return func(*args,**kwargs)
    return wrapper

@timer
@login_required
def dashboard(user=None):
    time.sleep(0.05)
    return 'ok'

# 测试
print(dashboard(user='克莱恩'))
dashboard()

