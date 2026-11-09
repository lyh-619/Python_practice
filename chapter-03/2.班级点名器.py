"""场景：老师上课要点名，学生名单是一个列表。"""

# 要求：
# 请实现一个 RollCall 类，让它成为一个迭代器
# 每次 next() 返回一个学生名字，点完所有人后抛出 StopIteration。

students = ['克莱恩','奥黛丽','伦纳德','佛尔思','休','格尔曼','卢米安','简','梅丽莎']

class RollCall:
    def __init__(self,students):
        self.students = students
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.students):
            raise StopIteration
        name = self.students[self.index]
        self.index += 1
        return name

rc = RollCall(students)
for name in rc:
    print(f'到，我是{name}')
