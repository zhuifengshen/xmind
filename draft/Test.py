
# 未知操作 但解决了包重名的冲突
import sys
# sys.path.insert(0, ".")
# print(sys.path)

import xmind
import search
# from xmind import core
from PyQt5.Qt import *
from xmind.core import topic
import numpy
import glob
def Test1():
    workbook = xmind.load('XmlTest.xmind')
    # print(workbook.getData());
    # print(workbook.to_prettify_json())

    sheet = workbook.getPrimarySheet()
    root_topic = sheet.getRootTopic()
    root_data = root_topic.getData()
    # 第一个分支主题
    test = root_topic.getSubTopicByIndex(0)
    # print(test.to_prettify_json())
    # print(test.to_prettify_json())

    # tops应该是两个标签组
    tops = test.getSubTopics()

    # for temp in tops:
    #     print(temp.to_prettify_json())
    # print(ttt[1].to_prettify_json())

    tData = tops[0].getData()
    # print(tops[0].getData()["title"])
    # ==========
    print(tops[0]._node)
    print(tops[0]._node.parentNode)
    print(tops[0]._node.childNodes)

    tem = topic.TopicsElement(tops[0]._node.parentNode,workbook)
    subtem = tem.getSubTopics()
    print(subtem[0].getTitle())
    # addlist = []
    # search.title_search(workbook, tops[0],addlist,"标签")
    # print(addlist)


    # topic01 = root_topic.getSubTopicByIndex(1)
    # tt = topic01.getSubTopicByIndex(1)
    # print(tt.getData())

    # sub_topic1 = root_topic.addSubTopic()
    # sub_topic1.setTitle("first sub topic")

    # xmind.save(workbook)

def pppnode():
    workbook = xmind.load('XmlTest.xmind')
    sheet = workbook.getPrimarySheet()
    root_topic = sheet.getRootTopic()
    root_data = root_topic.getData()
    # 第一个分支主题
    test = root_topic.getSubTopicByIndex(0)
    # tops应该是两个标签组
    tops = test.getSubTopics()

    # for temp in tops:
    #     print(temp.to_prettify_json())
    # print(ttt[1].to_prettify_json())

    # tData = tops[0].getData()
    # print(tops[0].getData()["title"])
    # ==========
    # print(tops[0]._node)
    # pnode = tops[0]._node.parentNode
    # print(pnode)
    # ppnode = pnode.parentNode
    # print(ppnode)
    # pppnode =ppnode.parentNode
    # print(pppnode)
    # print()
    # print(tops[0]._node.childNodes)

    # tem = topic.TopicElement(pppnode,workbook)
    # subtem = tem.getSubTopics()
    # print(subtem[0].getTitle())
    # print(tem.getData())

    addlist = []
    search.title_search(workbook, tops[0],addlist,"标签")
    print(addlist)

def test2():
    workbook = xmind.load('XmlTest.xmind')
    sheet = workbook.getPrimarySheet()
    root_topic = sheet.getRootTopic()
    # root_data = root_topic.getData()
    # # 第一个分支主题
    # test = root_topic.getSubTopicByIndex(0)
    # # tops应该是两个标签组
    # tops = test.getSubTopics()

    addlist = []
    search.title_search(workbook, root_topic, addlist, "子")
    # print(addlist)
    print("\n".join(str(i) for i in addlist))

def recursive_file_search():
     # print(glob.glob('**/*.xmind',recursive=True))
    print(glob.glob('D:\\SFTR\\**/*.xmind',recursive=True))
    print(glob.glob('D:\SFTR\**/*.xmind',recursive=True))

def getSubClasses(cls,level):
    for subcls in cls.__subclasses__():        # print(level)        
        print('--'*level,'|',subcls)
        if len(cls.__subclasses__())>0:
            getSubClasses(subcls,level+1)
    
    

if __name__ == '__main__':
    # getSubClasses(core.Node,1)
    # test2()
    # if []:
    #     print("1")
    # numpy.array()
    # for i in range(3):
    #     print(i)

    a =["asdf","2","23"]
    print(len(a[0]))