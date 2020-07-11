import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QHeaderView, QButtonGroup
from PyQt5.QtCore import QThread, pyqtSignal, QBasicTimer
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from ui import Ui_Form

class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.rootdir = ''
        self.step =0
        self.progressBar.setValue(self.step)
        self.timer = QBasicTimer()
        self.tableViewSet()

        ## 单选框
        self.bgr = QButtonGroup(self)
        self.bgr.addButton(self.rb1, 1)
        self.bgr.addButton(self.rb2, 2)

        self.bgr.buttonClicked.connect(self.rbclicked)
        self.addDirButton.clicked.connect(self.addFolder)
        self.searchButton.clicked.connect(self.search)
        

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            return
        print(self.step)
        self.step += 1
        self.progressBar.setValue(self.step)

    def addFolder(self):
        foldername = QFileDialog.getExistingDirectory(self, "选取文件夹", "C:/")
        self.lineEdit.setText(foldername)
    
    def tableViewSet(self):
        #设置数据层次结构，1行4列
        self.model= QStandardItemModel(1,4)
        self.model.setHorizontalHeaderLabels(['文件名','作者','标题','读取权限', '所属公司'])
        self.tableView.setModel(self.model)
        #水平方向标签拓展剩下的窗口部分，填满表格
        self.tableView.horizontalHeader().setStretchLastSection(True)
        #水平方向，表格大小拓展到适当的尺寸      
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def rbclicked(self):
        sd = self.sender()
        if sd == self.bgr:
            checkedID = self.bgr.checkedId()
            if checkedID == 1:
                self.fileSuffix = self.rb1.text()
            elif checkedID == 2:
                self.fileSuffix = self.rb2.text()
            else:
                self.fileSuffix = ''

    def process(self):
        try:
            folderPath = self.linEdit.text()
            print(folderPath)
        except:
            pass

    def search(self):
        self.tableView.clearSpans()
        self.rootdir = self.lineEdit.text()
        self.keyword = self.lineEdit_2.text()
        if self.rootdir == '':
            QMessageBox.warning(self, '查询提示', '输入的查询路径不能为空', QMessageBox.Yes)
            return False
        if self.keyword == '':
            QMessageBox.warning(self, '查询提示', '输入的关键字不能为空', QMessageBox.Yes)
            return False

        self.searchButton.setDisabled(True)
        try:
            senderData = (self.rootdir, self.lineEdit_2.text())
            self.Thread = FindFileThread(senderData)
            self.Thread.resultSearchSignal.connect(self.updateResult)
            self.Thread.start()
            self.actionPbar()
        except Exception as e:
            print(e)
    
    def actionPbar(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)


    def updateResult(self, resultData):
        self.searchButton.setDisabled(False)
        for data in resultData:
            # self.tableView.addItem(data)
            self.model.appendRow([
                QStandardItem(data),
                QStandardItem('zuozhe'),
                QStandardItem('f'),
                QStandardItem('chris'),
                QStandardItem('chris'),
            ])
        self.step = 100
        self.progressBar.setValue(self.step)
        self.timer.stop()

class FindFileThread(QThread):
    resultSearchSignal = pyqtSignal(list) # 声明一个带列表结果的参数信号

    def __init__(self, item):
        super(FindFileThread, self).__init__()
        self.dst, self.kw = item

    def initargs(self, rootdir, kw):
        self.dst = rootdir
        self.kw = kw

    def run(self):
        result = []
        files = self.search_file(self.dst, self.kw, False, False)
        for file in files:
            result.append(file)
        if not result:
            result = ['无查询结果']
        try:
            # 发射信号
            self.resultSearchSignal.emit(result)
        except Exception as e:
            print(e)

    def search_file(self, directory, patterns='*', single_level=False, yield_folders=False):
        patterns = [item.strip() for item in patterns.split(',')]
        try:
            for path, subdirs, files in os.walk(directory):
                if yield_folders:
                    files.extend(subdirs)
                files.sort()
                for name in files:
                    for pattern in patterns:
                        if pattern in name:
                            yield os.path.join(path, name)
                            break
                if single_level:
                    break
            else:
                return ''
        except Exception as e:
            raise e


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MyWindow()
    ui.show()
    sys.exit(app.exec_())