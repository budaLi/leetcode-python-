#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/13
#猜数字游戏 让游戏可以看到最近的几条输入 网站的历史记录
from collections import deque   #双端循环队列

def start_game(N):
    ans=66
    if N==ans:
        print('right')
        return True
    elif N>ans:
        print('big')
    else:
        print('small')
    return False

if __name__=='__main__':
    q=deque([],5)
    while True:
        print('请输入你的猜数,q查询输入记录')
        req=raw_input()
        if req=='q':
            print(q)
        else:
            req=int(req)
            q.append(req)
            if start_game(req):
                print('win')
                break
