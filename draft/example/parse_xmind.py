#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json

import xmind
import pipes


def custom_parse_xmind(workbook):
    elements = {}

    def _echo(tag, element, indent=0):
        title = element.getTitle()
        elements[element.getID()] = title
        print('\t' * indent, tag, ':', pipes.quote(title))

    def dump_sheet(sheet):
        root_topic = sheet.getRootTopic()
        _echo('RootTopic', root_topic, 1)

        for topic in root_topic.getSubTopics() or []:
            _echo('AttachedSubTopic', topic, 2)

        for topic in root_topic.getSubTopics(xmind.core.const.TOPIC_DETACHED) or []:
            _echo('DetachedSubtopic', topic, 2)

        for rel in sheet.getRelationships():
            id1, id2 = rel.getEnd1ID(), rel.getEnd2ID()
            print('Relationship: [%s] --> [%s]' % (elements.get(id1), elements.get(id2)))

    for sheet in workbook.getSheets():
        _echo('Sheet', sheet)
        dump_sheet(sheet)


def dict_to_prettify_json(data):
    print(json.dumps(data, indent=4, separators=(',', ': ')))


def main():
    # 1、you can convert the xmind file to dict data or json data
    workbook = xmind.load('demo.xmind')
    print(workbook.getData())
    print(workbook.to_prettify_json())

    # 2、you can also convert the sheet to dict data
    sheet = workbook.getPrimarySheet()
    dict_to_prettify_json(sheet.getData())

    # 3、as well as topic
    root_topic = sheet.getRootTopic()
    dict_to_prettify_json(root_topic.getData())

    # 4、as well as comments
    commentsbook = workbook.commentsbook
    print(commentsbook.getData())

    # 5、custom extraction of required data
    custom_parse_xmind(workbook)


if __name__ == '__main__':
    main()
