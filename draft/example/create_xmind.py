# -*- coding: utf-8 -*-

import xmind
from xmind.core.const import TOPIC_DETACHED
from xmind.core.markerref import MarkerId
from xmind.core.topic import TopicElement


def gen_my_xmind_file():
    # load an existing file or create a new workbook if nothing is found
    workbook = xmind.load("my.xmind")
    # get the first sheet(a new workbook has a blank sheet by default)
    sheet1 = workbook.getPrimarySheet()
    design_sheet1(sheet1)
    # create sheet2
    gen_sheet2(workbook, sheet1)
    # now we save as test.xmind
    xmind.save(workbook, path='test.xmind')


def design_sheet1(sheet1):
    # ***** first sheet *****
    sheet1.setTitle("first sheet")  # set its title

    # get the root topic of this sheet(a sheet has  a blank root topic by default)
    root_topic1 = sheet1.getRootTopic()
    root_topic1.setTitle("root node")  # set its title

    # create some sub topic element
    sub_topic1 = root_topic1.addSubTopic()
    sub_topic1.setTitle("first sub topic")

    sub_topic2 = root_topic1.addSubTopic()
    sub_topic2.setTitle("second sub topic")

    sub_topic3 = root_topic1.addSubTopic()
    sub_topic3.setTitle("third sub topic")

    sub_topic4 = root_topic1.addSubTopic()
    sub_topic4.setTitle("fourth sub topic")

    # create a detached topic(attention: only root topic can add a detached topic)
    detached_topic1 = root_topic1.addSubTopic(topics_type=TOPIC_DETACHED)
    detached_topic1.setTitle("detached topic")
    detached_topic1.setPosition(0, 30)

    sub_topic1_1 = sub_topic1.addSubTopic()
    sub_topic1_1.setTitle("I'm a sub topic too")


def gen_sheet2(workbook, sheet1):
    # ***** second sheet *****
    # create a new sheet and add to the workbook by default
    sheet2 = workbook.createSheet()
    sheet2.setTitle("second sheet")

    # a sheet has a blank sheet by default
    root_topic2 = sheet2.getRootTopic()
    root_topic2.setTitle("root node")

    # use other methods to create some sub topic element
    topic1 = TopicElement(ownerWorkbook=workbook)
    # set a topic hyperlink from this topic to the first sheet given by s1.getID()
    topic1.setTopicHyperlink(sheet1.getID())
    topic1.setTitle("redirection to the first sheet")  # set its title

    topic2 = TopicElement(ownerWorkbook=workbook)
    topic2.setTitle("topic with an url hyperlink")
    topic2.setURLHyperlink("https://github.com/zhuifengshen/xmind")  # set an url hyperlink

    topic3 = TopicElement(ownerWorkbook=workbook)
    topic3.setTitle("third node")
    topic3.setPlainNotes("notes for this topic")  # set notes (F4 in XMind)
    topic3.setTitle("topic with \n notes")

    topic4 = TopicElement(ownerWorkbook=workbook)
    topic4.setFileHyperlink("logo.png")  # set a file hyperlink
    topic4.setTitle("topic with a file")

    topic1_1 = TopicElement(ownerWorkbook=workbook)
    topic1_1.setTitle("sub topic")
    topic1_1.addLabel("a label")  # official XMind only can a one label

    topic1_1_1 = TopicElement(ownerWorkbook=workbook)
    topic1_1_1.setTitle("topic can add multiple markers")
    topic1_1_1.addMarker(MarkerId.starBlue)
    topic1_1_1.addMarker(MarkerId.flagGreen)

    topic2_1 = TopicElement(ownerWorkbook=workbook)
    topic2_1.setTitle("topic can add multiple comments")
    topic2_1.addComment("I'm a comment!")
    topic2_1.addComment(content="Hello comment!", author='devin')

    # then the topics must be added to the root element
    root_topic2.addSubTopic(topic1)
    root_topic2.addSubTopic(topic2)
    root_topic2.addSubTopic(topic3)
    root_topic2.addSubTopic(topic4)
    topic1.addSubTopic(topic1_1)
    topic2.addSubTopic(topic2_1)
    topic1_1.addSubTopic(topic1_1_1)

    # to loop on the subTopics
    topics = root_topic2.getSubTopics()
    for index, topic in enumerate(topics):
        topic.addMarker("priority-" + str(index + 1))

    # create a relationship
    sheet2.createRelationship(topic1.getID(), topic2.getID(), "relationship test")


if __name__ == '__main__':
    gen_my_xmind_file()
