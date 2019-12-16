#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QCheckBox, QWidget, QPushButton, QLabel, QLineEdit, QApplication, )


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        l_w = 50
        e_w = 220

        # 文本标签
        lab1 = QLabel('关键词', self)
        lab1.move(l_w, 40)
        lab2 = QLabel('微博账号', self)
        lab2.move(l_w, 80)
        lab3 = QLabel('微博密码', self)
        lab3.move(l_w, 120)
        self.label = QLabel('   验证码', self)
        self.label.setFixedSize(120, 40)
        self.label.move(l_w, 270)

        # 文本输入框

        self.edit1 = QLineEdit(self)
        self.edit1.move(e_w, 40)
        self.edit2 = QLineEdit(self)
        self.edit2.move(e_w, 80)
        self.edit3 = QLineEdit(self)
        self.edit3.move(e_w, 120)
        self.yzm_edit = QLineEdit(self)
        self.yzm_edit.move(e_w, 270)
        self.yzm_edit.textEdited.connect(self.onChange)

        # 复选框
        key_btn1 = QCheckBox('博主昵称', self)
        key_btn1.move(l_w, 170)
        key_btn2 = QCheckBox('博主主页', self)
        key_btn2.move(180, 170)
        key_btn3 = QCheckBox('微博内容', self)
        key_btn3.move(310, 170)
        key_btn4 = QCheckBox('发布时间', self)
        key_btn4.move(440, 170)
        key_btn5 = QCheckBox('微博地址', self)
        key_btn5.move(50, 220)
        key_btn6 = QCheckBox('微博来源', self)
        key_btn6.move(180, 220)
        key_btn7 = QCheckBox('转发，评论，赞', self)
        key_btn7.move(310, 220)

        self.bun = QPushButton('开始', self)
        self.bun.clicked.connect(self.start_btn_clicked)
        self.bun.move(200, 350)
        self.label.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:10px;font-weight:bold;font-family:宋体;}"
                                 )

        self.setGeometry(300, 300, 800, 450)
        self.setWindowTitle('微博关键字爬取系统')
        self.show()

    def start_btn_clicked(self):
        key = self.edit1.text()
        username = self.edit2.text()
        password = self.edit3.text()
        print(self.edit1.text())
        jpg = QtGui.QPixmap('1.png')
        self.label.setPixmap(jpg)

    def onChange(self):
        self.bun.setText('确认')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
