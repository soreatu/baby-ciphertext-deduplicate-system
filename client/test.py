import sys
import os
import config

from internel.api.api import Session
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from internel.utils.formatFileSize import formatFileSize
from internel.utils.CST2CommonTime import CST2CommonTime
from internel.utils.aes import AES
from internel.utils.sha1 import SHA1




'''pyqt5动态添加删除控件'''
class DynAddObject(QDialog):
    def __init__(self, parent=None):
        super(DynAddObject, self).__init__(parent)
        self.widgetList = []
        addButton = QPushButton(u"添加控件")
        delBUtton = QPushButton(u"删除控件")
        self.layout = QGridLayout()
        self.layout.addWidget(addButton, 1, 0)
        self.layout.addWidget(delBUtton, 2, 0)
        self.setLayout(self.layout)
        addButton.clicked.connect(self.add)
        delBUtton.clicked.connect(self.delete)

    def add(self):
        btncont= self.layout.count()
        widget = QPushButton(str(btncont-1), self)
        self.layout.addWidget(widget)
        
    def delete(self):
        for i in range(self.layout.count())[2:]:
            self.layout.itemAt(i).widget().deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = DynAddObject()
    form.show()
    app.exec_()





"""
class fileDialogdemo(QWidget):
    def __init__(self,parent=None):
        super(fileDialogdemo, self).__init__(parent)
        self.resize(400, 500)
        #垂直布局
        layout=QVBoxLayout()

        #创建按钮，绑定自定义的槽函数，添加到布局
        self.btn1=QPushButton('上传文件')
        self.btn1.clicked.connect(self.getFiles)
        layout.addWidget(self.btn1)

        #实例化多行文本框，添加到布局
        self.contents=QTextEdit()
        layout.addWidget(self.contents)

        #设置主窗口的布局及标题
        self.setLayout(layout)
        self.setWindowTitle('File Dialog 例子')

    def getFiles(self):
        #实例化QFileDialog
        dig=QFileDialog()
        #设置可以打开任何文件
        dig.setFileMode(QFileDialog.ExistingFiles)
        if dig.exec_():
            #接受选中文件的路径，默认为列表
            filenames=dig.selectedFiles()
            print(filenames)
            self.contents.setText(filenames[0])
            #列表中的第一个元素即是文件路径，以只读的方式打开文件
if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=fileDialogdemo()
    ex.show()
    sys.exit(app.exec_())
"""





"""
with open("/Users/jylsec/Desktop/实验周/client/key/key","wb") as f:
    f.write(AES(SHA1("jylsec".encode()).digest()[:16]).encrypt(b"jylsecjylsecjylsecjylsec"))
"""

"""
config.WORK_DIR = os.getcwd()
s = Session("http://127.0.0.1:8081/api/v1", "jylsec", "jylsec")

files, error = s.get_files()
if error:
    print(error)
else:
    for i in files:
        print([i["filename"] , formatFileSize(i["size"]) , CST2CommonTime(i["updated_at"])])
"""