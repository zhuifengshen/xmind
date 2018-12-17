#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import logging
import os
from tkinter import *
from tkinter import filedialog
from zentao.xmind_to_excel import XMindToExcel

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s  %(name)s  [%(module)s - %(funcName)s]  %(levelname)s: %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S')


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.home = os.path.dirname(os.path.realpath(__file__))
        self.createWidgets(master)

    def createWidgets(self, master=None):

        self.frame_1 = Frame(master)
        self.xmind_text = Text(self.frame_1, height="1", width="60")
        self.xmind_text.pack(side=LEFT, expand=YES)
        self.xmind_text.insert(INSERT, "XMind File Path")
        self.sp01_label = Label(self.frame_1, text='<==', height="1", width="5")
        self.sp01_label.pack(side=LEFT, expand=YES)
        self.select_file_button = Button(self.frame_1, text='选择文件', command=self.select_xmind_file)
        self.select_file_button.pack()
        self.frame_1.pack(side=TOP)

        self.frame_2 = Frame(master)
        self.excel_file_text = Text(self.frame_2, height="1", width="60")
        self.excel_file_text.pack(side=LEFT, expand=YES)
        self.excel_file_text.insert(INSERT, "生成目标路径")
        self.sp02_label = Label(self.frame_2, text='<==', height="1", width="5")
        self.sp02_label.pack(side=LEFT, expand=YES)
        self.excel_file_label = Label(self.frame_2, text='结果文件 ', height="1")
        self.excel_file_label.pack()
        self.frame_2.pack(side=TOP)

        self.frame_3 = Frame(master)
        self.template_text = Text(self.frame_3, height="1", width="60")
        self.template_text.pack(side=LEFT, expand=YES)
        self.template_text.insert(INSERT, "使用默认模板")
        self.sp03_label = Label(self.frame_3, text=u'<==', height="1", width="5")
        self.sp03_label.pack(side=LEFT, expand=YES)
        self.templet_file_button = Button(self.frame_3, text='选择模板', command=self.select_template_file)
        self.templet_file_button.pack()
        self.frame_3.pack(side=TOP)

        self.frame_4 = Frame(master)
        self.sp04_label = Label(self.frame_4, text=' ', height="1", width="80")
        self.sp04_label.pack(side=LEFT, expand=YES)
        self.frame_4.pack(side=TOP)

        self.frame_5 = Frame(master)
        self.start_button = Button(self.frame_5, text='Xmind转为Excel', state='disabled', command=self.xmind2excel)
        self.start_button.pack(side=LEFT, expand=YES)
        self.sp05_label = Label(self.frame_5, text=' ', height="1", width="5")
        self.sp05_label.pack(side=LEFT, expand=YES)
        self.quit_button = Button(self.frame_5, text='退出程序', command=self.quit)
        self.quit_button.pack(side=LEFT)
        self.frame_5.pack(side=TOP)

        self.frame_6 = Frame(master)
        self.sp06_label = Label(self.frame_6, text=' ', height="1", width="80")
        self.sp06_label.pack(side=LEFT, expand=YES)
        self.frame_6.pack(side=TOP)

    def select_xmind_file(self):
        xmind_filename = ""

        logging.info('初始选择路径：%s', os.path.join(self.home, 'template'))
        select_filename = filedialog.askopenfilename(initialdir=(os.path.join(self.home, 'template')))
        if len(select_filename) != 0 and os.path.splitext(select_filename)[1] == '.xmind':
            xmind_filename = select_filename
            message = "您选择的文件是：" + xmind_filename
        else:
            message = "您没有选择任何文件或者选择文件格式有误，请重新选择！"
        logging.info(message)

        self.xmind_text.delete(0.0, END)
        self.xmind_text.insert(1.0, xmind_filename if xmind_filename else message)

        src_path = os.path.dirname(xmind_filename)
        result_excel_file = os.path.join(src_path, "result.xlsx")
        self.excel_file_text.delete(0.0, END)
        self.excel_file_text.insert(1.0, result_excel_file)
        return xmind_filename

    def select_template_file(self):
        filenames = filedialog.askopenfilename(initialdir=(os.path.join(self.home, 'template')))
        if len(filenames) != 0:
            template_filename = filenames
            message = "您选择的模板是：" + template_filename
        else:
            template_filename = os.path.join(self.home, 'template/case_template.xlsx')
            message = "您没有选择任何模板，将使用默认模板：" + template_filename
        logging.info(message)

        template_suffix = os.path.splitext(template_filename)[1]
        xmind_text_suffix = os.path.splitext(self.xmind_text.get('1.0', END).strip())[1]
        self.template_text.delete(0.0, END)

        if template_suffix == ".xlsx" and xmind_text_suffix == '.xmind':
            self.template_text.insert(1.0, template_filename)
            self.start_button['state'] = 'normal'
        elif template_suffix == '.xls' and xmind_text_suffix == '.xmind':
            excel_file_text_content = self.excel_file_text.get('1.0', END).strip()
            excel_file_file_name = os.path.splitext(excel_file_text_content)[0]
            self.excel_file_text.delete(0.0, END)
            self.excel_file_text.insert(1.0, excel_file_file_name + template_suffix)
            self.template_text.insert(1.0, template_filename)
            self.start_button['state'] = 'normal'
        else:
            self.template_text.insert(1.0, '您选择的模板或XMind格式有误，请重新选择！')

        return template_filename

    def xmind2excel(self):
        xmind_file_path = self.xmind_text.get('1.0', END).strip()
        excel_file_path = self.excel_file_text.get('1.0', END).strip()
        template_file_path = self.template_text.get('1.0', END).strip()
        logging.info('Xmind测试用例文件：%s', xmind_file_path)
        logging.info('测试用例模板文件：%s', template_file_path)
        logging.info('开始将XMind文件转为为Excel文件：%s', excel_file_path)

        xmind_to_excel = XMindToExcel(xmind_file_path, excel_file_path, template_file_path)
        result = xmind_to_excel.main()
        msg = 'XMind To Excel Successfully!' if result else 'XMind To Excel Failed!'
        logging.info('Xmind测试用例转为Excel测试用例结果：%s', msg)
        self.sp06_label.config(text=msg)
        return result


if __name__ == '__main__':
    app = Application()
    # 窗口标题:
    app.master.title('Xmind测试用例转为Excel测试用例')
    app.master.geometry('800x600+100+100')
    # app.master.place(x=1000, y=1000)
    favicon_path = os.path.join(app.home, 'favicon.ico')
    app.master.iconbitmap(favicon_path)
    # 主消息循环:
    app.master.mainloop()
