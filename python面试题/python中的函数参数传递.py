#-*-coding:utf8-*-
#author : Lenovo
#date: 2019/1/5


#python中对象有两种类型 可变对象和不可变对象
#可变对象 如 list dic set 等 不可变对象如 数字 字符串以及元组


a=1
def test(a):
    a=2

b=[]
def test2(b):
    b.append(1)

if __name__=="__main__":
    test(a)
    print(a)

    test2(b)
    print(b)


#从上面两个例子中可以看出  当函数传递的是不可变参数时  函数对其操作无影响

#当参数类型为可变类型时  相当于对这个可变对象进行操作

