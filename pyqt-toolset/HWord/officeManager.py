"""
[Python and Microsoft Office – Using PyWin32](http://www.blog.pythonlibrary.org/2010/07/16/python-and-microsoft-office-using-pywin32/)
参考文件
https://stackoverflow.com/questions/56242873/how-to-get-the-revision-number-of-a-word-document-using-python
https://ios.developreference.com/article/12766171/Access+built-in+document+properties+information+without+opening+the+workbook
"""
import os
import sys
from enum import Enum
import win32com.client as win32c


class Properties:
    ct = 'Create Date'
    author = 'Author'
    # lastAuthor = 'Last Author'
    revision = 'Revision'
    owenCompany = 'Company'
    title = 'Title'
    scheme = 'Scheme'
    mark = 'Mark'
    manager = 'Manager'

    columnMap = {
            '标题': title,
            '作者': author,
            # '最后一次作者': lastAuthor, # 不能修改
            '所属公司': owenCompany
        }

    @classmethod
    def match(cls, key):
        return cls.columnMap.get(key, 'None')


class FileType:
    Word = 1
    Excel = 2

    @classmethod
    def match(cls, type_):
        key_map = {
            cls.Word: 'Word.Application',
            cls.Excel: 'Excel.Application',
        }
        return key_map[type_]

    @classmethod
    def suffix(cls, type_):
        return {
            cls.Word: ['docx', 'doc'],
            cls.Excel: ['xlsx']
        }[type_]


class OfficeMgr(object):
    def __init__(self):
        self.wd = None
        self.type = None
        self.client = None
        self.latestFile = ''
    
    def initType(self, type_):
        if self.type != type_:
            self.close()
        self.type = type_
        self.client = win32c.gencache.EnsureDispatch(FileType.match(self.type))
        self.client.Visible = False  # 

    def run(self, file):
        try:
            # if self.latestFile != '' and self.latestFile != file:
            #     # 关闭上一次打开的文件
            #     self.__wd.Close()
            if self.type == FileType.Word:
                self.wd = self.client.Documents.Open(os.path.realpath(file))
                self.builtInPro = self.wd.BuiltInDocumentProperties
            elif self.type == FileType.Excel:
                self.wd = self.client.Workbooks.Open(os.path.realpath(file))
                self.builtInPro = self.wd.BuiltinDocumentProperties
            else:
                pass
            return self
        except Exception as e:
            os.remove(os.path.realpath(file))
            print(f'正在删除异常文件：{file}')
            if self.wd:
                self.wd.Close(0)
                self.client.Quit()
            raise e

    def __del__(self):
        if self.wd:
            self.wd.Close(True)
            self.client.Quit()

    def get(self):
        result = {
        'title': self.builtInPro(Properties.title).value,
        'author': self.builtInPro(Properties.author).value,
        # 'lastAuthor': self.builtInPro(Properties.lastAuthor).value,
        'owenCompany': self.builtInPro(Properties.owenCompany).value
        }
        self.wd.Close()
        return result
    
    def set(self, key, val):
        p = Properties.match(key)
        if self.type == FileType.Word:
            self.wd.BuiltInDocumentProperties(p).value = val
            self.wd.Close()
        elif self.type == FileType.Excel:
            self.wd.BuiltinDocumentProperties(p).value = val
            self.wd.Close(True)

    def close(self):
        if self.client:
            self.client.Quit()

    
if __name__ == '__main__':
    ob = OfficeMgr()
    ob.initType(1)
    ob.run(r'C:\Users\asus\Desktop\word_dir\cds\testmongo.docx')
    res = ob.get()
    print(res)
    ob.run(r'C:\Users\asus\Desktop\word_dir\cds\testmongo.docx')
    ob.set('最后一次作者', 'JChri')

    ob.run(r'C:\Users\asus\Desktop\word_dir\cds\testmongo.docx')
    res = ob.get()
    print(res)
    ob.client.Quit()
