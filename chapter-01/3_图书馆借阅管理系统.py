"""场景描述：设计一个图书馆系统。"""
# 要求：
# 图书类：书名、ISBN、作者、是否可借
# 读者类：姓名、借书证号、已借图书列表；单人可以借多本，但有借阅上限
# 图书馆类：管理图书和读者，支持借书、还书、按条件查询
# 借书时校验：图书存在、可借、读者未超上限、同一本书不能重复借
# 还书时校验：读者确实借了这本书
# 支持 in 判断某本书是否在馆、len() 统计馆藏、for...in 遍历可借图书
# 图书可比较（按 ISBN 判等），可打印可读信息
# 提供类方法从字典批量创建图书

# 自定义异常基类
class LibraryError(Exception):
    pass

# 图书类
class Book:
    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.__available = True               # 私有属性：是否可借

    @property
    def available(self):
        return self.__available

    def _set_available(self, flag):           # 仅供内部调用
        self.__available = flag

    @classmethod
    def from_dict(cls, data):                 # 类方法批量构造
        return cls(data['isbn'], data['title'], data['author'])

    # 按 ISBN 判等
    def __eq__(self, other):
        return isinstance(other, Book) and self.isbn == other.isbn

    def __hash__(self):
        return hash(self.isbn)

    def __str__(self):
        state = '可借' if self.__available else '已借出'
        return f"《{self.title}》- {self.author} [ISBN:{self.isbn}] ({state})"

    def __repr__(self):
        return f"Book({self.isbn!r}, {self.title!r})"


# 读者类
class Reader:
    MAX_BORROW = 5                            # 借阅上限

    def __init__(self, card_id, name):
        self.card_id = card_id
        self.name = name
        self.__borrowed = []                  # 已借图书列表

    @property
    def borrowed(self):
        return list(self.__borrowed)          # 返回副本，防止外部篡改

    @property
    def borrow_count(self):
        return len(self.__borrowed)

    def can_borrow(self):
        return self.borrow_count < self.MAX_BORROW

    def _add_book(self, book):
        self.__borrowed.append(book)

    def _remove_book(self, book):
        self.__borrowed.remove(book)

    def __str__(self):
        titles = "、".join(f"《{b.title}》" for b in self.__borrowed) or "无"
        return f"读者[{self.card_id}] {self.name}，已借 {self.borrow_count} 本：{titles}"


# 图书馆类
class Library:
    def __init__(self, name):
        self.name = name
        self.__books = {}                     # isbn -> Book
        self.__readers = {}                   # card_id -> Reader

    # 注册
    def add_book(self, book):
        if book.isbn in self.__books:
            raise ValueError(f"图书 ISBN {book.isbn} 已存在")
        self.__books[book.isbn] = book

    def add_reader(self, reader):
        if reader.card_id in self.__readers:
            raise LibraryError(f"读者证号 {reader.card_id} 已存在")
        self.__readers[reader.card_id] = reader

    # 核心业务：借书
    def borrow(self, card_id, isbn):
        reader = self.__readers.get(card_id)
        if reader is None:
            raise LibraryError(f"读者 {card_id} 不存在")
        book = self.__books.get(isbn)
        if book is None:
            raise LibraryError(f"图书 ISBN {isbn} 不存在")
        if not book.available:
            raise LibraryError(f"《{book.title}》已被借出")
        if not reader.can_borrow():
            raise LibraryError(f"读者 {reader.name} 已达借阅上限 {Reader.MAX_BORROW} 本")
        if book in reader.borrowed:
            raise LibraryError(f"读者 {reader.name} 已借过《{book.title}》")

        book._set_available(False)
        reader._add_book(book)
        print(f"✔ {reader.name} 借阅《{book.title}》成功")

    # 核心业务：还书
    def return_book(self, card_id, isbn):
        reader = self.__readers.get(card_id)
        if reader is None:
            raise LibraryError(f"读者 {card_id} 不存在")
        book = self.__books.get(isbn)
        if book is None:
            raise LibraryError(f"图书 ISBN {isbn} 不存在")
        if book not in reader.borrowed:
            raise LibraryError(f"读者 {reader.name} 未借阅《{book.title}》")

        book._set_available(True)
        reader._remove_book(book)
        print(f"✔ {reader.name} 归还《{book.title}》成功")

    # 查询
    def search_by_author(self, author):
        return [b for b in self.__books.values() if b.author == author]

    # 魔术方法
    def __len__(self):
        return len(self.__books)

    def __contains__(self, isbn):
        return isbn in self.__books

    def __iter__(self):                       # 遍历可借图书
        return (b for b in self.__books.values() if b.available)

    def __str__(self):
        return f"图书馆[{self.name}] 藏书 {len(self)} 本，读者 {len(self.__readers)} 人"


# ---------- 测试 ----------
lib = Library("市立图书馆")

# 批量添加图书
books_data = [
    {"isbn": "978-1", "title": "Python 编程", "author": "张三"},
    {"isbn": "978-2", "title": "算法导论", "author": "李四"},
    {"isbn": "978-3", "title": "数据结构", "author": "张三"},
    {"isbn": "978-4", "title": "操作系统", "author": "王五"},
]
for d in books_data:
    lib.add_book(Book.from_dict(d))

r1 = Reader("R001", "小明")
r2 = Reader("R002", "小红")
lib.add_reader(r1)
lib.add_reader(r2)

print(lib)
print("-" * 40)

# 借书流程
lib.borrow("R001", "978-1")
lib.borrow("R001", "978-2")
lib.borrow("R001", "978-3")
try:
    lib.borrow("R001", "978-4")            # 超上限
except LibraryError as e:
    print("✘ 借书失败：", e)

try:
    lib.borrow("R002", "978-1")            # 已被借出
except LibraryError as e:
    print("✘ 借书失败：", e)

print("-" * 40)
print(r1)
print(r2)

# 还书 + 再借
lib.return_book("R001", "978-2")
lib.borrow("R002", "978-2")

print("-" * 40)
print("馆藏总数：", len(lib))
print("是否含 978-4：", "978-4" in lib)
print("可借图书遍历：")
for b in lib:
    print("  ", b)

print("按作者'张三'查询：", lib.search_by_author("张三"))