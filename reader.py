'''
Created on 2017年8月17日

@author: dykong
'''
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication,QWidget,QGridLayout,QTextBrowser,QFileDialog,QPushButton,\
    QMenuBar, QAction
from _functools import partial
import chardet

class example(QWidget):
    def __init__(self):
        super().__init__()
        self.encode='GBK'
        self.initUI()
    def initUI(self):
        self.setGeometry(300,300,300,200)
        self.setWindowTitle('reader')
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.5)  #设置透明度
      
        self.grid=QGridLayout()   #设置布局

        
        openAction=QAction('&open',self)    #菜单事件   
        openAction.triggered.connect(self.openText)
        opacityAction1=QAction('&25%',self)
        opacityAction1.triggered.connect(partial(self.opacity,0.25))
        opacityAction2=QAction('&50%',self)
        opacityAction2.triggered.connect(partial(self.opacity,0.5))
        opacityAction3=QAction('&75%',self)
        opacityAction3.triggered.connect(partial(self.opacity,0.75))
        opacityAction4=QAction('&100%',self)
        opacityAction4.triggered.connect(partial(self.opacity,1))

        menubar=QMenuBar()  #创建菜单
        self.openmenu=menubar.addMenu('&file') #添加菜单选项
        self.openmenu.addAction(openAction) #给菜单添加内容
        self.setopacity=menubar.addMenu('&opacity')#设置透明度
        self.setopacity.addAction(opacityAction1)
        self.setopacity.addAction(opacityAction2)
        self.setopacity.addAction(opacityAction3)
        self.setopacity.addAction(opacityAction4)

        self.textpart=QTextBrowser()
         
        self.grid.addWidget(menubar)
        self.grid.addWidget(self.textpart)
 
        self.setLayout(self.grid)
        self.show()
    

    def openText(self):  #打开文件操作
        
        self.filename,type=QFileDialog.getOpenFileName(self, '选取文件', 'C:/', 'Text Files (*.txt)') #选择文件
        print(self.filename,type)
        self.detectCode() #查看编码方式
        
        if self.encode=='GB2312':
            self.encode='GBK'
        print(self.encode)
        try:
            self.f=open(self.filename,'r',encoding=self.encode) #打开文件
            self.content=self.f.read() #读取文件
            self.textpart.setText(self.content) #显示在文本框中
            self.f.close() #关闭文件
        except Exception as e:
            print('error e')
    
    def opacity(self,num):
        self.setWindowOpacity(num)   

    def detectCode(self): #查看编码方式
        fc=open(self.filename,'rb') #二进制的方式打开文件
        line1=fc.readline()
        encf=chardet.detect(line1)
        self.encode=encf['encoding']
        print(self.encode)
        lines=fc.readlines() #读取文件
        if self.encode=='ascii':
            for line in lines:
                enc=chardet.detect(line) #查看文件信息 
                if enc['encoding']!=self.encode:
                    if enc['encoding']=='ISO-8859-9':
                        self.encode='GBK'
                        break
                    else:
                        self.encode=enc['encoding']
                        print(self.encode)
                        break        
        
        fc.close()    #关闭文件
if __name__=='__main__':
    app=QApplication(sys.argv)
    w=example()
    sys.exit(app.exec_())
    