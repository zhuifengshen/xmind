#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import xmind
import pipes

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


def main():
    x = xmind.load('test.xmind')
    for sheet in x.getSheets():
        _echo('Sheet', sheet)
        dump_sheet(sheet)


if __name__ == '__main__':
    main()
