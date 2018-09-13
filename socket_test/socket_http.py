#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/13
import urlparse
import socket

def get_url(url):
    url_pat=urlparse.urlparse(url)
    host=url_pat.netloc     #域名
    path=url_pat.path
    if path=='':
        path='/'
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((host,80))       #注意此处为元组  端口为80

    #注意此处的格式
    client.send("GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(path,host))

    date=b''    #二进制接受数据
    while True:
        d=client.recv(1024)
        if d:
            date+=d
        else:
            break

    date=date.decode('utf8')
    html_date=date.split('\r\n\r\n')[1]
    print(html_date)
    client.close()      #关闭链接


if __name__=='__main__':
    get_url('http://www.baidu.com')