# @Time    : 2019/9/19 13:56
# @Author  : Libuda
# @FileName: 按序打印.py
# @Software: PyCharm

import threading
import time
from queue import Queue


def printFirst():
    print("one")
    time.sleep(1)


def printSecond():
    print("second")
    time.sleep(1)


def printThird():
    print("third")
    time.sleep(1)


class Foo1(object):
    def __init__(self):
        pass

    def first(self, printFirst):
        """
        :type printFirst: method
        :rtype: void
        """

        # printFirst() outputs "first". Do not change or remove this line.
        printFirst()

    def second(self, printSecond):
        """
        :type printSecond: method
        :rtype: void
        """

        # printSecond() outputs "second". Do not change or remove this line.
        printSecond()

    def third(self, printThird):
        """
        :type printThird: method
        :rtype: void
        """

        # printThird() outputs "third". Do not change or remove this line.
        printThird()

    def main(self):
        th1 = threading.Thread(target=self.first, args=(printFirst,))
        th2 = threading.Thread(target=self.second, args=(printSecond,))
        th3 = threading.Thread(target=self.third, args=(printThird,))

        th1.start()
        th1.join()

        th2.start()
        th2.join()

        th3.start()
        th3.join()


if __name__ == "__main__":
    # 1
    S = Foo1()
    S.main()
