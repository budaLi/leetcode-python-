# coding:utf-8
# 验证码图像标注GUI

from PyQt5 import QtWidgets, QtCore, QtGui
import sys, os
import time
import traceback


class ImgTag(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("验证码图片标注")
        # 主控件和主控件布局
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_layout)

        # 图像展示控件
        self.img_widget = QtWidgets.QWidget()
        self.img_layout = QtWidgets.QHBoxLayout()
        self.img_widget.setLayout(self.img_layout)
        # 标签占位
        self.img_view = QtWidgets.QLabel("请选择一个文件夹！")
        self.img_view.setAlignment(QtCore.Qt.AlignCenter)
        self.img_layout.addWidget(self.img_view)

        # 图像标注控件
        self.img_input = QtWidgets.QLineEdit()
        self.img_input.returnPressed.connect(self.next_img_click)  # 回车事件绑定

        # 控制按钮控件
        self.opera_widget = QtWidgets.QWidget()
        self.opera_layout = QtWidgets.QVBoxLayout()
        self.opera_widget.setLayout(self.opera_layout)
        # 各个按钮
        self.select_img_btn = QtWidgets.QPushButton("选择目录")
        self.select_img_btn.clicked.connect(self.select_img_click)
        self.previous_img_btn = QtWidgets.QPushButton("上一张")
        self.previous_img_btn.setEnabled(False)
        self.previous_img_btn.clicked.connect(self.previous_img_click)
        self.next_img_btn = QtWidgets.QPushButton("下一张")
        self.next_img_btn.setEnabled(False)
        self.next_img_btn.clicked.connect(self.next_img_click)
        self.save_img_btn = QtWidgets.QPushButton("保存")
        self.save_img_btn.setEnabled(False)
        self.save_img_btn.clicked.connect(self.next_img_click)
        # 添加按钮到布局
        self.opera_layout.addWidget(self.select_img_btn)
        self.opera_layout.addWidget(self.previous_img_btn)
        self.opera_layout.addWidget(self.next_img_btn)
        self.opera_layout.addWidget(self.save_img_btn)

        # 将控件添加到主控件布局层
        self.main_layout.addWidget(self.img_widget, 0, 0, 4, 4)
        self.main_layout.addWidget(self.opera_widget, 0, 4, 5, 1)
        self.main_layout.addWidget(self.img_input, 4, 0, 1, 4)

        # 状态栏
        self.img_total_current_label = QtWidgets.QLabel()
        self.img_total_label = QtWidgets.QLabel()
        self.statusBar().addPermanentWidget(self.img_total_current_label)
        self.statusBar().addPermanentWidget(self.img_total_label, stretch=0)  # 在状态栏添加永久控件

        # 设置UI界面核心控件
        self.setCentralWidget(self.main_widget)

    # 选择目录按钮
    def select_img_click(self):
        try:
            self.dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, '选择文件夹')
            # print(self.dir_path)
            dir_list = os.listdir(self.dir_path)
            img_list = []
            for dir in dir_list:
                suffix_list = ['jpg', 'png', 'jpeg', 'bmp', ]
                if dir.split('.')[-1].lower() in suffix_list:
                    # print(dir)
                    img_list.append(dir)
            if len(img_list) > 0:
                # 图像文件索引字典
                self.img_index_dict = dict()
                for i, d in enumerate(img_list):
                    self.img_index_dict[i] = d
                # print(self.img_index_dict)
                self.current_index = 0  # 当前的图像索引
                # 当前图片文件路径
                self.current_filename = os.path.join(
                    self.dir_path, self.img_index_dict[self.current_index]
                )
                # 实例化一个图像
                image = QtGui.QImage(self.current_filename)
                self.img_width = image.width()  # 图片宽度
                self.img_height = image.height()  # 图片高度
                self.img_scale = 1
                self.image = image.scaled(self.img_width * self.img_scale, self.img_height * self.img_scale)

                # 在img_view控件中显示图像
                self.img_view.setPixmap(QtGui.QPixmap.fromImage(self.image))

                # 当前文件名
                self.current_text = self.img_index_dict[self.current_index].split('.')[0]

                # 设置img_input控件文本内容
                self.img_input.setText(self.current_text)
                self.img_input.setFocus()  # 获取输入框焦点
                self.img_input.selectAll()  # 全选文本

                # 启用其他按钮
                self.previous_img_btn.setEnabled(True)
                self.next_img_btn.setEnabled(True)
                self.save_img_btn.setEnabled(True)

                # 设置状态栏 图片数量信息
                self.img_total_current_label.setText("{}".format(self.current_index + 1))
                self.img_total_label.setText("/{total}".format(total=len(img_list)))

            else:
                QtWidgets.QMessageBox.information(
                    self, '提示', '文件夹没有发现图片文件！',
                    QtWidgets.QMessageBox.Ok
                )
        except Exception as e:
            print(repr(e))

    # 下一张图片
    def next_img_click(self):
        # 修改当前图像文件名
        new_tag = self.img_input.text()  # 获取当前输入框内容
        current_img = self.img_index_dict[self.current_index]  # 获取当前图片名称
        try:
            os.rename(
                os.path.join(self.dir_path, current_img),
                os.path.join(self.dir_path, new_tag + '.' + current_img.split('.')[-1])
            )  # 修改文件名
            self.img_index_dict[self.current_index] = new_tag + '.' + current_img.split('.')[-1]
        except FileExistsError as e:  # 同名文件异常
            print(repr(e))
            QtWidgets.QMessageBox.information(
                self, '提示', '已存在同名文件！',
                QtWidgets.QMessageBox.Ok
            )

        # 当前图像索引加1
        self.current_index += 1
        if self.current_index in self.img_index_dict.keys():
            # 当前图片文件路径
            self.current_filename = os.path.join(
                self.dir_path, self.img_index_dict[self.current_index]
            )
            # 实例化一个图像
            image = QtGui.QImage(self.current_filename)
            self.img_width = image.width()  # 图片宽度
            self.img_height = image.height()  # 图片高度
            self.img_scale = 1
            self.image = image.scaled(self.img_width * self.img_scale, self.img_height * self.img_scale)

            # 在img_view控件中显示图像
            self.img_view.setPixmap(QtGui.QPixmap.fromImage(self.image))
            # 当前文件名
            self.current_text = self.img_index_dict[self.current_index].split('.')[0]
            # 设置img_input控件文本内容
            self.img_input.setText(self.current_text)
            self.img_input.setFocus()  # 获取输入框焦点
            self.img_input.selectAll()  # 全选文本

            # 设置状态栏
            self.img_total_current_label.setText(str(self.current_index + 1))
        else:
            self.current_index -= 1
            QtWidgets.QMessageBox.information(
                self, '提示', '所有图片已标注完！',
                QtWidgets.QMessageBox.Ok
            )

    # 上一张图片
    def previous_img_click(self):
        # 修改当前图像文件名
        new_tag = self.img_input.text()  # 获取当前输入框内容
        current_img = self.img_index_dict[self.current_index]  # 获取当前图片名称
        try:
            os.rename(
                os.path.join(self.dir_path, current_img),
                os.path.join(self.dir_path, new_tag + '.' + current_img.split('.')[-1])
            )  # 修改文件名
            self.img_index_dict[self.current_index] = new_tag + '.' + current_img.split('.')[-1]
        except FileExistsError as e:  # 同名文件异常
            print(repr(e))
            QtWidgets.QMessageBox.information(
                self, '提示', '已存在同名文件！',
                QtWidgets.QMessageBox.Ok
            )

        # 当前图像索引加1
        self.current_index -= 1
        if self.current_index in self.img_index_dict.keys():
            # 当前图片文件路径
            self.current_filename = os.path.join(
                self.dir_path, self.img_index_dict[self.current_index]
            )
            # 实例化一个图像
            image = QtGui.QImage(self.current_filename)
            self.img_width = image.width()  # 图片宽度
            self.img_height = image.height()  # 图片高度
            self.img_scale = 1
            self.image = image.scaled(self.img_width * self.img_scale, self.img_height * self.img_scale)

            # 在img_view控件中显示图像
            self.img_view.setPixmap(QtGui.QPixmap.fromImage(self.image))
            # 当前文件名
            self.current_text = self.img_index_dict[self.current_index].split('.')[0]
            # 设置img_input控件文本内容
            self.img_input.setText(self.current_text)
            self.img_input.setFocus()  # 获取输入框焦点
            self.img_input.selectAll()  # 全选文本

            # 设置状态栏
            self.img_total_current_label.setText(str(self.current_index + 1))
        else:
            self.current_index += 1
            QtWidgets.QMessageBox.information(
                self, '提示', '图片列表到顶了！',
                QtWidgets.QMessageBox.Ok
            )

    # 重写鼠标滚轮事件
    def wheelEvent(self, event):
        # 如果按住了Ctrl
        if event.modifiers() == QtCore.Qt.ControlModifier:
            try:
                delta = event.angleDelta().y()
                if delta > 0:
                    self.img_scale += 0.25
                    self.image_scaled = self.image.scaled(self.img_width * self.img_scale,
                                                          self.img_height * self.img_scale)
                    self.img_view.setPixmap(QtGui.QPixmap.fromImage(self.image_scaled))
                    self.statusBar().showMessage("当前图片缩放比例为：{}%".format(self.img_scale * 100))
                elif delta < 0:
                    if self.img_scale > 0.25:
                        self.img_scale -= 0.25
                        self.image_scaled = self.image.scaled(self.img_width * self.img_scale,
                                                              self.img_height * self.img_scale)
                        self.img_view.setPixmap(QtGui.QPixmap.fromImage(self.image_scaled))
                        self.statusBar().showMessage("当前图片缩放比例为：{}%".format(self.img_scale * 100))
            except Exception as e:
                print(traceback.print_exc())
                print(repr(e))


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = ImgTag()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
