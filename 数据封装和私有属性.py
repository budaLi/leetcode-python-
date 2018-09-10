#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/10
class Date:
    def __init__(self,year,month,day):
        self.year=year
        self.month=month
        self.day=day
class User:
    def __init__(self,birthday):
        self._birthday=birthday

    def get_age(self):
        return 2018-self._birthday.year


# user=User(Date(2014,9,21))
# print(user.get_age())
# print(user.birthday)
#此时我们可以用对象调用其属性 birthday


#当我们给这个属性加_时 其就变为私有属性 只有在类的内部才可以访问
#但是这种方法并不是绝对访问不到的 甚至java中的私有属性的方法也可以通过反射机制获取到
#  user=User(Date(2014,9,21))
# print(user._birthday)       #会报错
