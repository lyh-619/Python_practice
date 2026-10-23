"""场景描述:设计一个银行账户系统，包含普通账户和储蓄账户。"""
# 要求：
# 普通账户支持存款、取款
# 储蓄账户继承普通账户，但取款时需保留最低余额 100 元
# 每次操作后能打印账户信息和交易记录

class RegularAccount:

    def __init__(self,owner,balance):
        self.owner = owner
        self.__balance = balance # 属性私有化
        # 建立一个空列表来记录交易
        self.history = []

    @property
    def balance(self):
        return self.__balance

    def deposit(self,amount):
        if amount <= 0:
            raise ValueError('存款金额必须大于0')
        else:
            self.__balance += amount
            self.history.append(f'本次交易存款{amount}元，余额剩余{self.__balance}')

    def withdraw(self,amount):
        if amount > self.__balance:
            raise ValueError('对不起，您的余额不足！')
        else:
            self.__balance -= amount
            self.history.append(f'本次交易取款{amount}元，余额剩余{self.__balance}')

    def show_info(self):
        print(f'账户持有人：{self.owner}\n余额：{self.__balance}')

class SavingsAccount(RegularAccount):

    MIN_BALANCE = 100 # 余额最低不能小于100

    def withdraw(self,amount):
        if self.balance - amount < self.MIN_BALANCE:
            raise ValueError(f'储蓄账户最少要保留余额{self.MIN_BALANCE}元')
        super().withdraw(amount)

acct = SavingsAccount('张三',500)

acct.deposit(500)
acct.withdraw(800)
acct.show_info()

print(acct.history)








