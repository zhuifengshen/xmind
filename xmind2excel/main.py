#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
from tkinter import *
from tkinter import filedialog


FILE_PATH = os.path.dirname(os.path.realpath(__file__))


def file_extension(path):
    return os.path.splitext(path)[1]


def file_name(path):
    return os.path.splitext(path)[0]


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets(master)

    def createWidgets(self, master=None):

        self.frame_1 = Frame(master)
        self.xmind_Text = Text(self.frame_1, height="1", width="60")
        self.xmind_Text.pack(side=LEFT, expand=YES)
        self.xmind_Text.insert(INSERT, "XMind file path")
        self.sp01_Label = Label(self.frame_1, text='<==', height="1", width="5")
        self.sp01_Label.pack(side=LEFT, expand=YES)
        self.select_file_button = Button(self.frame_1, text='选择文件', command=self.selectXmindFile)
        self.select_file_button.pack()
        self.frame_1.pack(side=TOP)

        self.frame_2 = Frame(master)
        self.excel_file_Text = Text(self.frame_2, height="1", width="60")
        self.excel_file_Text.pack(side=LEFT, expand=YES)
        self.excel_file_Text.insert(INSERT, "目标路径")
        self.sp02_Label = Label(self.frame_2, text='<==', height="1", width="5")
        self.sp02_Label.pack(side=LEFT, expand=YES)
        self.excel_file_Label = Label(self.frame_2, text='生成xls ', height="1")
        self.excel_file_Label.pack()
        self.frame_2.pack(side=TOP)

        self.frame_3 = Frame(master)
        self.templet_Text = Text(self.frame_3, height="1", width="60")
        self.templet_Text.pack(side=LEFT, expand=YES)
        self.templet_Text.insert(INSERT, "使用默认模板")
        self.sp03_Label = Label(self.frame_3, text=u'<==', height="1", width="5")
        self.sp03_Label.pack(side=LEFT, expand=YES)
        self.templet_file_button = Button(self.frame_3, text='选择模板', command=self.selectTempletFile)
        self.templet_file_button.pack()
        self.frame_3.pack(side=TOP)

        self.frame_4 = Frame(master)
        self.change_toxlsx_Button = Button(self.frame_4, text='Xmind转为xlsx', state='disabled', command=self.doxmind2xls)
        self.change_toxlsx_Button.pack(side=LEFT, expand=YES)
        self.sp04_Label = Label(self.frame_4, text=' ', height="1", width="5")
        self.sp04_Label.pack(side=LEFT, expand=YES)
        self.change_Button = Button(self.frame_4, text='Xmind转为xls', state='disabled', command=self.doxmind2xls)
        self.change_Button.pack(side=LEFT, expand=YES)
        self.sp05_Label = Label(self.frame_4, text=' ', height="1", width="5")
        self.sp05_Label.pack(side=LEFT, expand=YES)
        self.quitButton = Button(self.frame_4, text='Quit', command=self.quit)
        self.quitButton.pack(side=LEFT)
        self.frame_4.pack(side=TOP)

        self.frame_5 = Frame(master)
        self.sp05_Label = Label(self.frame_5, text=' ', height="1", width="80")
        self.sp05_Label.pack(side=LEFT, expand=YES)
        self.frame_5.pack(side=TOP)

    def selectXmindFile(self):
        string_filename = ""
        print((os.path.join(FILE_PATH, 'template')))

        filenames = filedialog.askopenfilename(initialdir=(os.path.join(FILE_PATH, 'template')))
        print(filenames)
        if len(filenames) != 0:
            string_filename = filenames
            text = "您选择的文件是：" + string_filename
        else:
            text = "您没有选择任何文件"
        print(text)
        self.xmind_Text.delete(0.0, END)
        self.xmind_Text.insert(
            1.0, string_filename if string_filename else text)

        src_path = os.path.dirname(string_filename)
        excel_file = os.path.join(src_path, "result.xls")
        excel_file = excel_file.replace("\\", "/")
        self.excel_file_Text.delete(0.0, END)
        self.excel_file_Text.insert(1.0, excel_file)
        return string_filename

    def selectTempletFile(self):
        string_filename = ""
        filenames = filedialog.askopenfilename(
            initialdir=(os.path.join(FILE_PATH, 'template')))
        print(filenames)
        if len(filenames) != 0:
            string_filename = filenames
            text = "您选择的模板是：" + string_filename
        else:
            text = "您没有选择任何模板，将继续使用默认模板"
        print(text)
        templet_extension = file_extension(string_filename)

        excel_file_Text_content = (self.excel_file_Text.get('1.0', END)).strip()
        excel_file_file_name = file_name(excel_file_Text_content)
        self.templet_Text.delete(0.0, END)
        self.templet_Text.insert(
            1.0, string_filename if string_filename else text)
        if templet_extension == ".xlsx":
            self.change_Button['state'] = 'disabled'
            self.change_toxlsx_Button['state'] = 'normal'
            self.excel_file_Text.delete(0.0, END)
            self.excel_file_Text.insert(
                1.0, excel_file_file_name + templet_extension)
        else:
            self.change_Button['state'] = 'normal'
            self.change_toxlsx_Button['state'] = 'disabled'
        return string_filename

    def doxmind2xls(self):
        xmind_Text_content = (self.xmind_Text.get('1.0', END)).strip()
        excel_file_Text_content = (self.excel_file_Text.get('1.0', END)).strip()
        templet_Text_content = (self.templet_Text.get('1.0', END)).strip()

        if templet_Text_content == "使用默认模板" or templet_Text_content == "使用默认模板" or templet_Text_content == "您没有选择任何模板，将继续使用默认模板":
            templet_Text_content = os.path.join(FILE_PATH, 'template/example.xls')
            templet_Text_content = templet_Text_content.replace("\\", "/")
            print(">>" * 10)
            pass
        temp_houzhui = file_extension(templet_Text_content)
        result = "fail"
        if temp_houzhui == ".xlsx":
            from xmind2excel.xmind2xlsx import XmindParse
            xmindParse = XmindParse(xmind_Text_content, excel_file_Text_content, templet_Text_content)
            result = xmindParse.main()
            pass
        else:
            from xmind2excel.xmind2xls import XmindParse
            xmindParse = XmindParse(xmind_Text_content, excel_file_Text_content, templet_Text_content)
            result = xmindParse.main()
            pass

        self.sp05_Label.config(text=result)
        print("**" * 10)
        return "ok"


if __name__ == '__main__':
    app = Application()
    # 窗口标题:
    app.master.title('Xmind测试用例转为Excel测试用例')
    favicon_path = os.path.join(FILE_PATH, 'favicon.ico')
    app.master.iconbitmap(favicon_path)
    # 主消息循环:
    app.master.mainloop()
