# -*- encoding: utf-8 -*-
'''
@DESCRIPTION : GUI implement 
@AUTHOR      : jylsec
@TIME        : 2021/06/17
'''

from PyQt5.QtWidgets import QGridLayout,QDialog, QFileDialog, QLabel, QMessageBox, QDesktopWidget, QPushButton, QVBoxLayout, QCheckBox
from PyQt5 import QtCore
from internel.api.api import Session
from internel.utils.formatFileSize import formatFileSize
from internel.utils.CST2CommonTime import CST2CommonTime


class GUI(QDialog):
    def __init__(self,parent=None):
        super(GUI, self).__init__(parent)
        self.s = Session("http://127.0.0.1:8081/api/v1", "jylsec", "jylsec")
        self.initUI(self.s.error)
    # 初始化ui
    def initUI(self,error):
        if error == 0:
            self.resize(200,100)
            self.setWindowTitle('WARNING!')
            self.text = QLabel("连接失败",alignment=QtCore.Qt.AlignCenter)
            layout = QVBoxLayout()
            layout.addWidget(self.text)
            self.setLayout(layout)
        else:    
            # resize()方法调整窗口的大小。这里是1000px长500px高               
            self.resize(1000, 500)
            # 窗口居中
            self.moveToCenter()
            # 设置标题
            self.setWindowTitle('Quiver')
            # 创建三种按钮
            uploadButton = QPushButton("上传文件")
            uploadButton.clicked.connect(self.uploadFile)
            downloadButton = QPushButton("下载文件")
            downloadButton.clicked.connect(self.downloadFile)
            deleteButton = QPushButton("删除文件")
            deleteButton.clicked.connect(self.deleteFile)
            self.layout = QGridLayout()
            self.layout.addWidget(uploadButton,1,0)
            self.layout.addWidget(downloadButton,1,1)
            self.layout.addWidget(deleteButton,1,2)
            self.updateCbBoxes()
            self.setLayout(self.layout)
    
    # 窗口显示在屏幕中心
    def moveToCenter(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 二次确认关闭窗口
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',"Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def updateCbBoxes(self):
        round = 2
        for i in range(self.layout.count())[3:]:
            self.layout.itemAt(i).widget().deleteLater()
        files,error = self.s.get_files()
        self.checkBoxes = {}
        for file in files:
            self.checkBoxes[int(file["id"])] = PowerfulCheckBox(int(file["id"]),str(file["filename"]),formatFileSize(file["size"]),CST2CommonTime(file["updated_at"]))
            self.layout.addWidget(self.checkBoxes[int(file["id"])],round,0)
            round += 1
    
    # 子窗口
    def callChildWindow(self,text):
        childWindow = ChildWindow()
        childWindow.setWindowTitle('提示')
        content = QLabel(text,alignment=QtCore.Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(content)
        childWindow.setLayout(layout)
        childWindow.show()
        childWindow.exec_()
        
    # 上传功能
    def uploadFile(self):
        uploadResults = []
        childWindowText = ""
        #实例化QFileDialog
        dig=QFileDialog()
        #设置可以打开任何文件
        dig.setFileMode(QFileDialog.ExistingFiles)
        if dig.exec_():
            #接受选中文件的路径，默认为列表
            filenames=dig.selectedFiles()
            for filename in filenames:
                childWindowText += filename + ": " + str(self.s.upload_file(filename)) + "\n"
                self.updateCbBoxes()
            if childWindowText != "":
                self.callChildWindow(childWindowText)
    
    # 删除文件
    def deleteFile(self):
        deleteFileIds = []
        childWindowText = ""
        for i in self.checkBoxes:
            if self.checkBoxes[i].isChecked():
                deleteFileIds.append(i) 
        if deleteFileIds != []:
            for i in deleteFileIds:
                childWindowText += self.checkBoxes[i].filename + ": " + str(self.s.delete_file(i)) + "\n"
                self.updateCbBoxes()
            self.callChildWindow(childWindowText)

    def downloadFile(self):
        dowloadFileIds = []
        childWindowText = ""
        for i in self.checkBoxes:
            if self.checkBoxes[i].isChecked():
                dowloadFileIds.append(i)
        if dowloadFileIds != []:
            for i in dowloadFileIds:
                childWindowText += self.checkBoxes[i].filename + ": " + str(self.s.download_file(i,self.checkBoxes[i].filename)) + "\n"
            self.callChildWindow(childWindowText)

class ChildWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.resize(400, 300)
class PowerfulCheckBox(QCheckBox):
    def __init__(self,id,filename,size,updated_at):
        super().__init__(filename + " ———— " + size + " ———— " + updated_at)
        self.id = id
        self.filename = filename
        