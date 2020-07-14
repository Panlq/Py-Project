#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = '__JonPan__'

import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QFileDialog, QMessageBox, QHeaderView, QMenu, QDialog,
                            QButtonGroup, QAbstractItemView, QTableWidgetItem)
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QBasicTimer, Qt
from PyQt5.QtGui import QStandardItemModel, QIcon, QPixmap

import resource
from main_ui import Ui_MainWindow
from modify_ui import Ui_Dialog
from officeManager import OfficeMgr, FileType, Properties


class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)
        self.rootdir = ''
        self.step =0
        self.fileDict = {}
        self.progressBar.setValue(self.step)
        self.timer = QBasicTimer()
        self.tableWidgetSet()
        self.setIcon()
        ## 单选框
        self.bgr = QButtonGroup(self)
        self.bgr.addButton(self.rb1, FileType.Word)
        self.bgr.addButton(self.rb2, FileType.Excel)

        self.bgr.buttonClicked.connect(self.rbclicked)
        self.addDirButton.clicked.connect(self.addFolder)
        self.searchButton.clicked.connect(self.search)

        # 
        self.omg = OfficeMgr()

    def setIcon(self):
        self.setWindowIcon(QIcon(':/img/hword.ico'))
        # icon = QIcon()
        # filename = self.resource_path(os.path.join('img', 'aqx2y-3232.ico'))
        # # filename = 'img/aqx2y-6464.ico'
        # icon.addPixmap(QPixmap(filename), QIcon.Normal, QIcon.Off)
        # self.setWindowIcon(icon)

    def resource_path(self, relative_path):
        if getattr(sys, 'frozen', False): 
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)   
    
    def closeEvent(self, event):
        # 显示两个框，一个是YES 一个NO，默认选中no
        reply = QMessageBox.question(self,"消息","确定要退出？",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)

        if reply == QMessageBox.Yes:
            # 接受事件
            event.accept()
        else:
            # 忽略事件
            event.ignore()    
        

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            return
        self.step += 1
        self.progressBar.setValue(self.step)

    def addFolder(self):
        foldername = QFileDialog.getExistingDirectory(self, "选取文件夹", "C:/")
        self.lineEdit.setText(foldername)

    def bindTableHeader(self):
        headerColumn = ['文件名']
        headerColumn.extend(list(Properties.columnMap.keys()))
        self.tableWidget.setHorizontalHeaderLabels(headerColumn)
    
    def tableWidgetSet(self):
        # 设置表头
        self.bindTableHeader()
        #水平方向，表格大小拓展到适当的尺寸      
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 表格设置成不可编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 只允许列选中
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectColumns)
        # 只允许单个选中
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        # 允许右键产生菜单
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        # 将右键菜单绑定到槽函数generateMenu
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)
        #显示下方水平的进度条
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn) 
        #隐藏竖直进度条
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def generateMenu(self, pos):
        # 计算选中的数据
        selected = self.tableWidget.selectionModel().selection().indexes()
        if len(selected) <= 1 or selected[-1].row() == 0 or selected[-1].column() == 0:
            # QMessageBox.warning(self, '查询提示', '未选中任何数据', QMessageBox.Yes)
            return False

        menu = QMenu()
        item1 = menu.addAction('批量修改')
        action = menu.exec_(self.tableWidget.mapToGlobal(pos))
    
        if action == item1:
            selected_col = selected[0].column()
            column_val = self.tableWidget.horizontalHeaderItem(selected_col).text()
            self.selected_key = column_val
            self.callModifyDialog()
            # QMessageBox.warning(self, '查询提示', '选中的列名', QMessageBox.Yes)

    def callModifyDialog(self):
        self.mdwindow = ModifyWindow(self)
        #
        self.mdwindow.resultModifySignal.connect(self.applyModify)
        self.mdwindow.show()

    def applyModify(self, resultData):
        _, newVal = resultData
        self.step = 0
        selected = self.tableWidget.selectionModel().selection().indexes()
        totalTask = len(selected)
        self.mdwindow.close()
        for i, item in enumerate(selected[1:]):
            row_num = item.row()
            fileName = self.getItemVal(row_num, 0)
            filePath = self.fileDict.get(fileName)
            self.omg.run(filePath).set(self.selected_key, newVal)
            self.step = ((i+2) / totalTask) * 100
            self.progressBar.setValue(self.step)
        # if self.step == 100:
        #     reply = MessageBoxTip.inof(self, '修改状态', '修改成功是否刷新')

        self.updataTableWidget(selected)


    def getItemVal(self, row_num, column_num):
        # 获取表格内容
        return self.tableWidget.item(row_num, column_num).text()

    def rbclicked(self):
        sd = self.sender()
        if sd == self.bgr:
            checkedID = self.bgr.checkedId()
            if checkedID == FileType.Word:
                self.fileSuffixType = FileType.Word                
            elif checkedID == FileType.Excel:
                self.fileSuffixType = FileType.Excel
            else:
                self.fileSuffixType = 0

    def process(self):
        try:
            folderPath = self.linEdit.text()
            print(folderPath)
        except:
            pass

    def search(self):
        self.tableWidget.clearContents()
        self.rootdir = self.lineEdit.text()
        self.keyword = self.lineEdit_2.text()
        if self.rootdir == '':
            QMessageBox.warning(self, '查询提示', '输入的查询路径不能为空', QMessageBox.Yes)
            return False
        if self.keyword == '':
            QMessageBox.warning(self, '查询提示', '输入的关键字不能为空', QMessageBox.Yes)
            return False

        self.searchButton.setDisabled(True)
        self.progressBar.setValue(0)
        try:
            senderData = (self.rootdir, self.lineEdit_2.text(), self.fileSuffixType)
            self.Thread = FindFileThread(senderData)
            self.Thread.resultSearchSignal.connect(self.updateResult)
            self.Thread.start()
            self.resetTableWidget()
            self.actionPbar()
        except Exception as e:
            print(e)
    
    def actionPbar(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)

    def updateResult(self, resultData):
        if not resultData[0]:
            self.step = 100
            MessageBoxTip.wanrning(self, '查询状态', resultData[1])
            self.progressBar.setValue(self.step)
        else:
            self.omg.initType(self.fileSuffixType)
            self.catchedFile = resultData[-1]
            self._writeRowData(self.catchedFile)
        self.searchButton.setDisabled(False)
        self.timer.stop()
    
    def updataTableWidget(self, selected):
        self.resetTableWidget()
        self._writeRowData(self.catchedFile)

    def resetTableWidget(self):
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(4)

    def _writeRowData(self, files):
        totalFiles = len(files)
        if totalFiles < 1:
            return
        curRowCount = self.tableWidget.rowCount() 
        for i, file in enumerate(files):
            filename = os.path.basename(file)
            self.fileDict[filename] = file
            self.step = ((i + 1) / totalFiles) * 100
            self.progressBar.setValue(self.step)
            item = self.omg.run(file).get()
            self.tableWidget.insertRow(curRowCount)
            self.tableWidget.setItem(curRowCount, 0, QTableWidgetItem(filename))
            self.tableWidget.setItem(curRowCount, 1, QTableWidgetItem(item['title']))
            self.tableWidget.setItem(curRowCount, 2, QTableWidgetItem(item['author']))
            self.tableWidget.setItem(curRowCount, 3, QTableWidgetItem(item['owenCompany']))


class FindFileThread(QThread):
    resultSearchSignal = pyqtSignal(tuple) # 声明一个带列表结果的参数信号

    def __init__(self, item):
        super(FindFileThread, self).__init__()
        self.dst, self.kw, self.fileSuffixType = item

    def initargs(self, rootdir, kw):
        self.dst = rootdir
        self.kw = kw

    def run(self):
        result = []
        flag = True
        files = self.search_file(self.dst, self.kw, False, False)
        for file in files:
            result.append(file)
        if not result:
            flag = False
            result = '无查询结果'
        try:
            # 发射信号
            self.resultSearchSignal.emit((flag, result))
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
                    suffix = name.split('.')[-1]
                    for pattern in patterns:
                        if pattern in name and (suffix in FileType.suffix(self.fileSuffixType)):
                            yield os.path.join(path, name)
                            break
                if single_level:
                    break
            else:
                return ''
        except Exception as e:
            raise e


class ModifyWindow(QtWidgets.QDialog, Ui_Dialog):
    resultModifySignal = pyqtSignal(tuple)
    def __init__(self, mainw):
        super(ModifyWindow, self).__init__()
        self.setupUi(self)
        self.val = ''
        # 设置窗口为模态，用户只有关闭弹窗后，才能关闭主界面
        self.setWindowModality(Qt.ApplicationModal)
        self.mainw = mainw

    @pyqtSlot()
    def accept(self):
        self.val = self.newValue.text()
        self.resultModifySignal.emit((1, self.val))


class MessageBoxTip:
    resultMessageBox = pyqtSignal(int)
    @classmethod
    def wanrning(cls, obj, title, text):
        QMessageBox.warning(obj, title, text, QMessageBox.Yes)
        return True

    @classmethod
    def inof(cls, obj, title, text):
        reply = QMessageBox.information(obj, title, text, QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        return reply
        
    @classmethod
    def tips(cls, obj, event, title, text):
        # 显示两个框，一个是YES 一个NO，默认选中no
        reply = QMessageBox.question(obj, title, text, QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 接受事件
            event.accept()
        else:
            # 忽略事件
            event.ignore()
        # self.resultMessageBox.emit(reply)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mui = MyMainWindow()
    mui.show()
    sys.exit(app.exec_())