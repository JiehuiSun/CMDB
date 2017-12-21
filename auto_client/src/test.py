# 约束实现该接口的类中必须定义xxx方法 --------- Python没有其他语言有
# interface IFoo:
#     def exec(self):pass
#
#
# class A(IFoo): # 实现IFoo,接口中的方法必须在当前类中实现
#
#     def exec(self):
#         pass
#
# class B(IFoo):
#     def exec(self):
#         pass
#
# def func(arg):
#     arg.exec()
#
# obj = A()
# func(obj)

# 抽象类： 接口约束的特性；类继承的特性
# 抽象类
# AbstractClass Foo:
#
#     # 抽象方法，
#     def abstractmethod exec():pass
#
#     def bar():
#         pass
#         pass
#
#
# class A(Foo): # 当前类继承了抽象类，期中必须定义抽象类中的所有抽象方法
#
#     def exec(self):
#         pass
#
# class B(Foo):
#     def exec(self):
#         pass
#
# def func(arg):
#     arg.exec()



"""
from abc import abstractmethod,ABCMeta

class Foo(metaclass=ABCMeta):

    @abstractmethod
    def exec(self):pass

class A(Foo):
    pass

obj = A()
"""

"""
class Foo(object):
    def exec(self):
        raise NotImplementedError('请实现exec方法')
class A(Foo):
    pass

obj = A()
obj.exec()
"""
















