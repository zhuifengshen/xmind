#!/usr/bin/env python
# -*- coding: utf-8 -*-

import XmindCopilot
from ..core import const
import glob
import re
import os

class Pointer(object):
    def __init__(self):
        # path - list of topic titles
        self.path = []
        # snapshot - record pathstr for CLI display
        self.snapshot = []

    def getpathstr(self):
        """获取当前路径String"""
        str = ""
        for p in self.path:
            str += p + "->"
        return str

    def printer(self):
        """打印当前路径"""
        print(self.getpathstr())

    def treeprint(self):
        """DEPRECATED 结构化打印当前路径 仅保留最后一项"""
        if self.path:
            tab = ""
            for i in range(len(self.path)-1):
                tab += "\t|"
            print(tab+self.path[-1])

    def snap(self, simplify=False):
        """记录当前路径并添加至self.snapshot"""
        if simplify:
            result = ""
            path = self.getpathstr()
            if self.snapshot:
                priouspath = self.snapshot[-1]
                flag = 1
                for i in range(len(path)):
                    if i < len(priouspath):
                        if path[i] == priouspath[i] and flag:
                            # result += " "
                            pass
                        else:
                            flag = 0
                            result += path[i]
                    else:
                        result += path[i]
            print(result)
            self.snapshot.append(result)
        else:
            self.snapshot.append(self.getpathstr())


# ==============Title_search
def topic_search(topic, str, depth: int = -1, re_match=False):
    # Search for title(return fisrt topic matched)
    title = topic.getTitle()
    # print(title,'\n')
    if title and (re_match and re.match(str, title) or str in title):
        return topic

    subtopiclist = topic.getSubTopics()
    if depth == -1 and subtopiclist:
        for t in subtopiclist:
            if topic_search(t, str):
                return topic_search(t, str)
    elif depth > 0 and subtopiclist:
        for t in subtopiclist:
            if topic_search(t, str, depth=depth-1):
                return topic_search(t, str, depth=depth-1)
        
    return None


def topic_search_snap(topic, ptr, str):
    title = topic.getTitle()
    if title:
        ptr.path.append(title)
        # 是否包含在标题中(正则表达式)
        if re.match(str, title):
            ptr.snap()
            # ptr.treeprint()
            # 并没有节省时间？
            # ptr.path.pop()
            # return
    else:
        ptr.path.append("[Title Empty]")

    subtopiclist = topic.getSubTopics()
    if subtopiclist:
        for t in subtopiclist:
            topic_search_snap(t, ptr, str)
    ptr.path.pop()
    return


def getTopicAddress(topic):
    """
    获取目标topic在workbook中的路径(停用)
    """
    connectsym = "->"
    route = ""
    parent = topic
    type = parent.getType()
    while type != const.TOPIC_ROOT:
        title = parent.getTitle()
        if title:
            route = title + connectsym + route
        else:
            route = "#FIG#" + connectsym + route
        parent = parent.getParentTopic()
        type = parent.getType()
    title = parent.getTitle()
    route = title + connectsym + route
    return route


# ================Xmind File Search

def getXmindPath():
    # print(glob.glob('**/*.xmind',recursive=True))
    # print(glob.glob('D:\\SFTR\\**/*.xmind',recursive=True))
    # print(glob.glob('D:\SFTR\**/*.xmind',recursive=True))
    # print(glob.glob('"D:\SFTR\**/*.xmind"',recursive=True))
    path = []
    path += glob.glob('D:/SFTR/**/*.xmind', recursive=True)
    path += glob.glob('E:/SFTRDatapool2/ProjectCompleted/**/*.xmind',
                      recursive=True)
    # print(path)
    return path


def workbooksearch(path, str):
    workbook = XmindCopilot.load(path)
    sheets = workbook.getSheets()
    SearchFetch = []
    if sheets[0].getTitle():
        for sheet in sheets:
            root_topic = sheet.getRootTopic()
            ptr = Pointer()
            # 目前此函数只能从roottopic开始
            topic_search_snap(root_topic, ptr, str)
            SearchFetch += ptr.snapshot
    else:
        if os.path.isfile(path):
            print("File doesn't exist:"+workbook.get_path())
        else:
            print("Failed to open:"+workbook.get_path())
    return SearchFetch


# ================Global Search

def GlobalSearch(searchstr, printoutput=1):
    """
    在SFTR和CompletedProject中搜索关键词
    """
    paths = getXmindPath()
    contentXmindFilePath = []  # 有搜索结果的文件
    contentlist = []
    for path in paths:
        SearchFetch = workbooksearch(path, searchstr)
        if SearchFetch:
            contentlist.append(path)
            contentXmindFilePath.append(path)
            contentlist += SearchFetch

    # if contentlist:
    #     contentlist = remove_duplicates(contentlist)

    if printoutput == 1:
        # print("\n".join(str(i) for i in contentXmindFilePath))
        # print("\n")
        print("\n".join(str(i) for i in contentlist))

    return contentlist


def GlobalSearchLooper():
    while 1:
        searchstr = input("Search:")
        if searchstr == "exit":
            break
        GlobalSearch(searchstr)
        # os.startfile("XmlTest.xmind")


def main():
    workbooksearch("D:/SFTR/1 Course/Mathematics/20200708 工科数学分析.xmind", "无穷级数")
    # GlobalSearchLooper()
    # GlobalSearch("贝叶斯")
    
    # workbook = xmind.load("E:/CodeTestFile/comprehensive-coding/XmindCopilot/test/XmlTest.xmind")
    # sheets = workbook.getSheets()
    # if not sheets[0].getTitle():
    #     print("Failed to open:"+workbook.get_path())
    # # SearchFetch = []
    # # for sheet in sheets:
    # root_topic = sheets[0].getRootTopic()
    # topic = topic_search(root_topic, "标签测试")
    # print("result:", topic.getTitle())
    pass


if __name__ == "__main__":
    main()
    pass
