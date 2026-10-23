"""设计一个简易电商系统"""
# 要求:
# 商品类：名称、单价、数量
# 购物车类：支持添加商品（同商品累加数量）、移除商品、计算总价、清空
# 支持 for ... in 遍历购物车中商品
# 商品对象能直接打印为可读字符串，且两个相同商品可判等
# 提供类方法从字典快速创建商品

class Product:

    def __init__(self,name,price,num = 1):
        self.name = name
        self.price = price
        self.num = num

    @property
    def subtotal(self):
        return self.price *self.num

    @classmethod
    def from_dict(cls,data):
        return cls(data['name'],data['price'],data['num'])

    def __add__(self, other):
        if self.name != other.name:
            raise ValueError('不是同一个商品')
        return Product(self.name,self.price,self.num + other.num)


    def __str__(self) -> str:
        return f'商品名称：{self.name}\n商品单价：{self.price}\n商品数量：{self.num}'

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value,Product) and self.name == value.name

class Cart:

    def __init__(self):
        self.items = {}

    def add_product(self,product):
        if product.name in self.items:
            self.items[product.name] = self.items[product] + product
        else:
            self.items[product.name] = product

    def add(self, product):
        if product.name in self.items:
            self.items[product.name] = self.items[product.name] + product
        else:
            self.items[product.name] = product

    def remove(self, name):
        self.items.pop(name, None)

    @property
    def total(self):
        return sum(p.subtotal for p in self.items.values())

    def clear(self):
        self.items.clear()

    def __iter__(self):
        return iter(self.items.values())

    def __len__(self):
        return len(self.items)

    def __str__(self):
        lines = [str(p) for p in self]
        return "\n".join(lines) + f"\n合计：{self.total} 元"

cart = Cart()
cart.add(Product("苹果", 5, 3))
cart.add(Product.from_dict({"name": "香蕉", "price": 3,'num':1}))
cart.add(Product("苹果", 5, 2))  # 自动累加数量

print(cart)
print("商品种类数：", len(cart))
for p in cart:
    print("遍历：", p)







