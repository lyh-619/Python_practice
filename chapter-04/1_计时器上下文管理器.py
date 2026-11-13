from time import time
import time
from types import TracebackType

class Timer:
    def __init__(self):
        self._start = None
        self.elapsed = None

    def __enter__(self):
        self._start = time.time()
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None):
        self.elapsed = time.time() - self._start
        self._start = None
        return False

t = Timer()
# 正常计时
with t:
    sum(range(1_000_000))
print(f'耗时{t.elapsed}s')
# 异常时间同样记录，且异常持续抛出
try:
    with t:
        raise ValueError('数据爆炸')
except ValueError as e:
    print(f'异常{e!r}已捕获，耗时{t.elapsed}s')

# 同一实例复用，第二次覆盖第一次
with t:
    time.sleep(0.05)
print(f'第二次耗时{t.elapsed}s')