#-*-coding:utf8-*-
#author : Lenovo
#date: 2019/1/5

#python3中 静态方法和实例方法使用时均需要实例化对象 否则会报错
#类方法可以直接采用类名加点的方法使用
class A():
    @classmethod
    def show(self):
        print(123)


if __name__=="__main__":
    A.show()