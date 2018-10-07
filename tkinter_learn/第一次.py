#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/7
import tkinter as tk
from PIL import Image,ImageTk

class App(object):
    def __init__(self,master):
        frame=tk.Frame(master)  #容器里可以存放tk,TK()对象
        frame.pack(side=tk.LEFT,padx=10,pady=10)

        self.button=tk.Button(frame,text='你好',bg='white',fg='blue',command=self.say)
        self.button.pack()
        self.show_image()


    def say(self):
        self.lable=tk.Label(text='么么哒')
        self.lable.pack()

    def show_image(self):
        image=Image.open(r'1.jpg')
        self.image=ImageTk.PhotoImage(image)   #image对象需要放在lable中
        self.lable=tk.Label(text='气度小',image=self.image,compound=tk.CENTER,fg='red')
        self.lable.pack()
root=tk.Tk()
app=App(root)
root.mainloop()

