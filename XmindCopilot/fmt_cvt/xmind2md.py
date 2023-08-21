# encoding: utf-8

import search
import XmindCopilot
import os
from typing import Dict
import typing as typing
import sys

import glob


def WalkTopic(dictXmind: Dict, resultDict: Dict):
    strTitle: typing.AnyStr = dictXmind['title']
    if 'topics' in dictXmind:
        pass
        # print(dictXmind['topics'])

        listTopics : typing.List = dictXmind['topics']

        if(listTopics.__len__() > 0):
            resultDict[strTitle] = {}
            for topic in listTopics:
                WalkTopic(topic, resultDict[strTitle])
    else:
        resultDict[strTitle] = strTitle

def Print2MDList(dictOri: typing.Dict) -> typing.AnyStr:
    levelOri = 0
    listStr = []

    def Print2MDListInternal(dictContent: typing.Dict, level):
        if type(dictContent).__name__ != 'dict':
            return
        level = level + 1
        for topic, topicDict in dictContent.items():
            listStr.append('  ' * (level - 1))
            listStr.append('- ')
            if topic:
                listStr.append(topic.replace('\n', '\t'))
            else:
                listStr.append('*FIG*')
            listStr.append('\n')
            Print2MDListInternal(topicDict, level)

    Print2MDListInternal(dictOri, levelOri)

    return ''.join(listStr)

def xmindfiles_cvt(paths):

    for path in paths:
        pathSource = path
        pathSource = pathSource.replace('\\', '/')
        # pathOutput = pathSource.split('/')[-1].split('.')[0] + '.xmind.md'
        #输出到原文件目录
        pathOutput = pathSource + '.md'
        strResult = ''

        # 有待更新链接算法！
        wikilinkpaths = glob.glob(os.path.dirname(pathSource).replace('\\', '/')+'/**/*.xmind',recursive=False)
        for file_path in wikilinkpaths:
            file_path = os.path.splitext(file_path)[0].replace('\\', '/')
            file_name = file_path.split('/')[-1]
            # print(file_name)
            strResult += '[['+file_name+'.xmind]]\n'

        workbook = XmindCopilot.load(pathSource)
        sheets = workbook.getSheets()
        for sheet in sheets:
            dictSheet = sheet.getData()
            dictResult: Dict = {}
            WalkTopic(dictSheet['topic'], dictResult)

            strResult += Print2MDList(dictResult)

        with open(pathOutput, 'w', encoding='utf-8') as f:
            f.write(strResult)
            print('Successfully wrote result into file: ' + pathOutput)

def test():
    print('sys.argv: ', sys.argv, "\n")

    pathSource = None
    pathOutput = None

    for i, val in enumerate(sys.argv):
        if(val == '-source'):
            pathSource = sys.argv[i + 1]
        if(val == '-output'):
            pathOutput = sys.argv[i + 1]

    pathSource = pathSource.replace('\\', '/')

    if pathOutput == None:
        # pathOutput = pathSource.split('/')[-1].split('.')[0] + '.xmind.md'
        #输出到原文件目录
        # pathOutput = pathSource.split('.xmind')[0] + '.xmind.md'
        pathOutput = pathSource + '.md'

    workbook = XmindCopilot.load(pathSource)
    sheet = workbook.getPrimarySheet()
    dictSheet = sheet.getData()
    dictResult: Dict = {}
    WalkTopic(dictSheet['topic'], dictResult)

    strResult = Print2MDList(dictResult)

    with open(pathOutput, 'w', encoding='utf-8') as f:
        f.write(strResult)
        print('Successfully wrote result into file: ' + pathOutput)

    # print(strResult)
    # print(dictSheet)

if __name__ == "__main__":
    # test()
    paths = search.getXmindPath()

    # paths = glob.glob('../**/*.xmind',recursive=True)
    print(paths)
    xmindfiles_cvt(paths)

