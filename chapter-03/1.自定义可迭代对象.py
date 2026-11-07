"""自定义可迭代对象"""
# 需求：实现一个 Countdown 类，可以被 for 循环遍历，从 N 倒数到 1

# 提示：
# 区分「可迭代对象（iterable）」和「迭代器（iterator）」两个概念。
# 需要实现 __iter__，它应返回一个迭代器（可以是自身，也可以是新对象）。
# 如果返回自身，还需要实现 __next__，并在末尾抛出 StopIteration。
# 思考点：如果 Countdown 对象被遍历两次（for 两次），会发生什么？如何让它可重复遍历？

class Countdown:
    def __init__(self,n):
        self.n = n
        self.index = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.index >= self.n:
            raise StopIteration
        value = self.n - self.index
        self.index += 1
        return value

for s in Countdown(10):
    print(s)

