#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import xmind
import pipes

M = {}


def _echo(tag, element, indent=0):
    title = element.getTitle()
    M[element.getID()] = title
    print '\t' * indent, tag, ':', pipes.quote(title)


def dump_sheet(sheet):
    rootTopic = sheet.getRootTopic()
    _echo('RootTopic', rootTopic, 1)

    for topic in rootTopic.getSubTopics() or []:
        _echo('AttachedSubTopic', topic, 2)

    for topic in rootTopic.getSubTopics(xmind.core.const.TOPIC_DETACHED) or []:
        _echo('DetachedSubtopic', topic, 2)

    for rel in sheet.getRelationships():
        id1, id2 = rel.getEnd1ID(), rel.getEnd2ID()
        print 'Relation: [%s] --> [%s]' % (M.get(id1), M.get(id2))


def main():
    x = xmind.load('test2.xmind')
    for sheet in x.getSheets():
        _echo('Sheet', sheet)
        dump_sheet(sheet)


if __name__ == '__main__':
    main()