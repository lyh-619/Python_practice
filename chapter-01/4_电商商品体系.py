"""需求：有普通商品、打折商品、限购商品。三者都有价格，但计算最终价格方式不同：
普通商品：原价
打折商品：原价 × 折扣
限购商品：超过限额部分加价
设计类结构，并写一个结算函数，接收商品列表返回总价。"""
from abc import ABC, abstractmethod

# 提示：
# 抽象出 get_final_price(quantity) 方法
# 限购商品的逻辑需要"数量"参数，注意基类方法签名要统一（这是多态的关键约束）
# 思考：如果新增一种"满减商品"，需要改动哪些地方？这体现了什么设计原则？
class Product(ABC):
    def __init__(self,name,price):
        self.name = name
        self._price = price

    @property
    def price(self):
        return self._price

    @abstractmethod
    def get_final_price(self,quantity):
        pass


class NormalProduct(Product):

    def get_final_price(self,quantity):
        return self.price * quantity

class DiscountProduct(Product):
    # 增加折扣 discount 参数
    def __init__(self,name,price,discount):
        super().__init__(name, price)
        self.discount = discount

    def get_final_price(self,quantity):
        return self.price * quantity * self.discount

class LimitProduct(Product):
    def __init__(self,name,price,limited_edition,limited_price):
        # 增加限量 limited_edition,超额的价格 limited_price 两个参数
        super().__init__(name, price)
        self.limited_edition = limited_edition
        self.limited_price = limited_price


    def get_final_price(self,quantity):
        if quantity > self.limited_edition:
            return self.price * self.limited_edition + self.limited_price * (quantity - self.limited_edition)
        else:
            return self.price * quantity



